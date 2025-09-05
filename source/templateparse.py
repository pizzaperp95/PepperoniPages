# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages HTML Template Parser, Version 0.1
# Handles parsing the templates for variables and other such goodies.

import sys
from peplib import *

debugMode = str_to_bool(sys.argv[2])

tempfile = "../temp/file.temp"
templatefile = sys.argv[1]
filename = tempfile
openedfile = []
defaultTitle = "Generated with Pepperoni Pages by PizzaPerpetrator"

def getDefaultTitle():
    global defaultTitle
    for i, val in enumerate(templatefile):
        if len(val) > 0:
            tempvar = val.strip().lower().split('=')
            if (tempvar == "<titledefault"):
                defaultTitle = tempvar.split('>')[0]
                print(defaultTitle)

def setTitleInPage():
    pass

# Main function, duh.
def main():
    pass


if __name__=="__main__":
    main()