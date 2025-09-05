# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages Shared Functions Library, Version 0.1
# Has several shared functions.

import sys

def str_to_bool(str):
    if (str.upper() == "TRUE"):
        return True
    else:
        return False

def striplines(filename):
    # Turn the file into an array, where each element of that array is one line of the file.
    with open(filename, 'r', encoding='UTF-8') as file:
        openedfile = [line.rstrip('\n') for line in file]
    return openedfile

