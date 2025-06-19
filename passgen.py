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

import secrets
import string

VERSION = 1
DEFAULT_CHARSET = string.ascii_letters + string.digits + '!@#$%^&*()-_=+[]{}<>?'
DEFAULT_LENGTH = 24

def passgen(charset:str=DEFAULT_CHARSET, length:int=DEFAULT_LENGTH):
    password = ''.join(secrets.choice(charset) for _ in range(length))
    return password

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=f'passgen v{VERSION} for secure password generating by imKokoT using secrets module! see https://github.com/imKokoT')
    parser.add_argument('-l', '--length', type=int, default=DEFAULT_LENGTH, help=f'password length; default {DEFAULT_LENGTH}', required=False)
    parser.add_argument('-c', '--charset', type=str, default=DEFAULT_CHARSET, help=f'password charset; default {DEFAULT_CHARSET.replace('%','%%')}', required=False)
    args = parser.parse_args()

    print(passgen(args.charset, args.length))
