#!/usr/bin/env python3

########################################################################################
#   MIT License                                                                        #
#                                                                                      #
#   Copyright (c) 2025 imKokoT                                                         #
#                                                                                      #
#   Permission is hereby granted, free of charge, to any person obtaining a copy       #
#   of this software and associated documentation files (the "Software"), to deal      #
#   in the Software without restriction, including without limitation the rights       #
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell          #
#   copies of the Software, and to permit persons to whom the Software is              #
#   furnished to do so, subject to the following conditions:                           #
#                                                                                      #
#   The above copyright notice and this permission notice shall be included in all     #
#   copies or substantial portions of the Software.                                    #
#                                                                                      #
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR         #
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,           #
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE        #
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER             #
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,      #
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE      #
#   SOFTWARE.                                                                          #
########################################################################################

import re
import secrets
import string

VERSION = 2

# --- SETTINGS ------------------------------------------------------------------------------------------
DEFAULT_LENGTH = 24                        # default password length; default 24
COPY_TO_CLIPBOARD = True                   # if True and run as app, it will copy password to clipboard; default True
SYMBOLS_CHARSET = '!@#$%^&*()-_=+[]{}<>?'  # charset of default ascii symbols; key `s`
# -------------------------------------------------------------------------------------------------------

DEFAULT_FORMAT = f'{{{DEFAULT_LENGTH}}}'
DEFAULT_CHARSET = string.ascii_letters + string.digits + SYMBOLS_CHARSET
ALPHABET_LOWER_CHARSET = string.ascii_lowercase
ALPHABET_UPPER_CHARSET = string.ascii_uppercase
HEX_LOWER_CHARSET = string.hexdigits.replace('ABCDEF', '')
HEX_UPPER_CHARSET = string.hexdigits.replace('abcdef', '')
DIGITS_CHARSET = string.digits
ALPHADIGITS_CHARSET = string.ascii_letters + string.digits
EXTENDED_SYMBOLS_CHARSET = string.punctuation # includes dots etc
OCT_CHARSET = string.octdigits
# i just hate regex
PLACEHOLDER_PATTERN = re.compile(r'(?<!\\){((?:[^}\\]|\\.)*?)}(?!})')
CUSTOM_PATTERN = re.compile(r'(?<!\\)\[((?:[^\]\\]|\\.)*?)\](?!\])')
EXCLUDE_PATTERN = re.compile(r'!(?<!\\)\[((?:[^\]\\]|\\.)*?)\](?!\])')


def passgen(format:str=f'{{{DEFAULT_LENGTH}}}') -> str:
    '''returns generated password as string
    
    Args:
        format (str): format of password
            ### how `format` works
            generated chars replaces instead of `{}`. you can write rule in it to format output result. 
            symbols out of `{}` will be static. use `\\{` and `\\}` to 
            place braces out of placeholder. number in braces describes how many symbols to generate. 
            if format is wrong, will raise ValueError or handle it as static string.

            for example `{16}` returns password of `DEFAULT_CHARSET` symbols with length 16.

            you can use presets of different charsets; write it after length. for example
            `{8 x}-{4 x}-4{3 x}-{1 [89ab]}{3 x}-{12 x}` returns UUID like format in lowercase.

            ### charsets
            you can combine charsets. duplicates don't affect to probability. example `{16 A a d [-+$%=\\[\\]/]}`
            - A -> ascii upper letters
            - a -> ascii lower letters
            - d -> digits
            - X -> upper hex
            - x -> lower hex
            - s -> symbols from `SYMBOLS_CHARSET`
            - S -> extended symbols that includes dot, coma etc
            - o -> oct
            - [] -> your symbols in `[]`; `\\[`, `\\]`, `\\{` and `\\}` to use them as target symbols
            
            ### excluding symbols
            if you use some build-in charsets you can also exclude symbols with `![]`. for example
            `{16 A a s ![-_/]}` returns password without `-`, `_` and `/`
    
    Raises:
        ValueError: if wrong format
    '''
    format = format.replace('\\{', '\ufff0').replace('\\}', '\ufff1')
    placeholdersRules = re.findall(PLACEHOLDER_PATTERN, format)
    for p in placeholdersRules:
        rules = p.strip().split(' ')
        if not rules or rules and not rules[0].isdigit(): 
            raise ValueError(f'placeholder "{{{p}}}" must have length as first rule!')
        
        length = int(rules[0])

        if len(rules) == 1:
            format = re.sub(
                PLACEHOLDER_PATTERN,
                lambda m: ''.join(secrets.choice(DEFAULT_CHARSET) for _ in range(length)),
                format, count=1)
            continue

        charset = set()
        for rule in rules[1:]:
            match rule:
                case 'A': charset.update(ALPHABET_UPPER_CHARSET)
                case 'a': charset.update(ALPHABET_LOWER_CHARSET)
                case 'd': charset.update(DIGITS_CHARSET)
                case 'X': charset.update(HEX_UPPER_CHARSET)
                case 'x': charset.update(HEX_LOWER_CHARSET)
                case 's': charset.update(SYMBOLS_CHARSET)
                case 'S': charset.update(EXTENDED_SYMBOLS_CHARSET)
                case 'o': charset.update(OCT_CHARSET)
                case _:
                    if re.match(CUSTOM_PATTERN, rule):
                        charset.update(
                            re.findall(CUSTOM_PATTERN, rule)[0].replace('\\[', '[').replace('\\]', ']')
                        )
                    elif re.match(EXCLUDE_PATTERN, rule):
                        charset.difference_update(
                            re.findall(EXCLUDE_PATTERN, rule)[0].replace('\\[', '[').replace('\\]', ']')
                        )
                    else:
                        continue
        
        if not charset:
            raise ValueError(f'charset of {{{p}}} is empty!')

        format = re.sub(
            PLACEHOLDER_PATTERN,
            lambda m: ''.join(secrets.choice(tuple(charset)) for _ in range(length)),
            format, count=1)
        
    return format.replace('\ufff0', '{').replace('\ufff1', '}')


if __name__ == "__main__":
    import argparse
    try:
        import clipboard
    except ModuleNotFoundError:
        if COPY_TO_CLIPBOARD:
            COPY_TO_CLIPBOARD = False
            print(f'{COPY_TO_CLIPBOARD=} because you didn\'t install "clipboard" module to copy. please `pip install clipboard`')

    parser = argparse.ArgumentParser(description=f'passgen v{VERSION} for secure password generating by imKokoT using `secrets` module! see https://github.com/imKokoT. if you think that this micro-project deserves more attention, just star it, thanks!')
    parser.add_argument('-f', '--format', type=str, default=DEFAULT_FORMAT, help=f'format of password; default "{DEFAULT_FORMAT}"', required=False)
    parser.add_argument('-c', '--count', type=int, default=1, help=f'how many passwords to generate', required=False)

    args = parser.parse_args()
    pwds = ''
    try:
        while args.count:
            pwd = passgen(args.format)
            print(pwd)
            pwds += pwd + '\n'
            args.count -= 1
    except ValueError as e:
        print(f'ERROR: {e}')
        exit(1)
    if COPY_TO_CLIPBOARD: clipboard.copy(pwds.strip())
