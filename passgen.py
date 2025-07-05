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
DEFAULT_LENGTH = 24         # default password length; default 24
COPY_TO_CLIPBOARD = True    # If True and run as app, it will copy password to clipboard; default True
SYMBOLS_CHARSET = '!@#$%^&*()-_=+[]{}<>?'
DEFAULT_CHARSET = string.ascii_letters + string.digits + SYMBOLS_CHARSET
# -------------------------------------------------------------------------------------------------------

DEFAULT_FORMAT = f'{{{DEFAULT_LENGTH}}}'
ALPHABET_LOWER_CHARSET = string.ascii_lowercase
ALPHABET_UPPER_CHARSET = string.ascii_uppercase
HEX_LOWER_CHARSET = string.hexdigits.replace('ABCDEF', '')
HEX_UPPER_CHARSET = string.hexdigits.replace('abcdef', '')
DIGITS_CHARSET = string.digits
ALPHADIGITS_CHARSET = string.ascii_letters + string.digits
PLACEHOLDER_PATTERN = r'(?<!\\){([a-zA-Z0-9\s]*)}'


def __rep(match):
    return match.group(1).strip()


def passgen(format:str=f'{{{DEFAULT_LENGTH}}}') -> str:
    '''returns generated password as string
    
    Args:
        format (str): format of password
            ### how `format` works

            generated chars replaces instead of `{}`. you can write rule in it to format output result. 
            you can use any other symbols out of `{}` to make it different format. use `\\{` and `\\}` to 
            place braces out of placeholder. number in braces describes how many symbols to generate.

            for example `{16}` returns password of `DEFAULT_CHARSET` symbols with length 16.

            you can use presets of different charsets; write it after length. for example
            `{8 x}-{4 x}-{4 x}-{4 x}-{12 x}` returns UUID like format in lowercase.

            ### charsets
            you can combine charsets. example `{16 A a d c[-+$%=\\[\\]/]}`
            - A -> ascii upper letters
            - a -> ascii lower letters
            - d -> digits
            - X -> upper hex
            - x -> lower hex
            - s -> symbols from `SYMBOLS_CHARSET`
            - c[] -> your symbols in `[]`; `\\[` `\\]` to use them as target symbols. duplicates will be removed
    '''
    placeholdersRules = re.findall(PLACEHOLDER_PATTERN, format.replace('\\{', '\ufff0').replace('\\}', '\ufff1'))
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
            break

        charset = set()
        for rule in rules[1:]:
            match rule:
                case 'A': charset.update(ALPHABET_UPPER_CHARSET)  
                case 'a': charset.update(ALPHABET_LOWER_CHARSET)  
                case 'd': charset.update(DIGITS_CHARSET)  
                case 'X': charset.update(HEX_UPPER_CHARSET)  
                case 'x': charset.update(HEX_LOWER_CHARSET)  
                case 's': charset.update(SYMBOLS_CHARSET)  
                case 'c': raise NotImplementedError('soon')
         
        format = re.sub(
            PLACEHOLDER_PATTERN,
            lambda m: ''.join(secrets.choice(tuple(charset)) for _ in range(length)),
            format, count=1)
        
    return format.replace('\\{', '{').replace('\\}', '}')


if __name__ == "__main__":
    import argparse
    try:
        import clipboard
    except ModuleNotFoundError:
        COPY_TO_CLIPBOARD = False
        print(f'{COPY_TO_CLIPBOARD=} because you don\'t install "clipboard" module to copy. please pip install clipboard')

    parser = argparse.ArgumentParser(description=f'passgen v{VERSION} for secure password generating by imKokoT using secrets module! see https://github.com/imKokoT')
    parser.add_argument('-f', '--format', type=str, default=DEFAULT_FORMAT, help=f'format of password; default "{DEFAULT_FORMAT}"', required=False)
    args = parser.parse_args()

    pwd = passgen(args.format)
    print(pwd)
    if COPY_TO_CLIPBOARD: clipboard.copy(pwd)
