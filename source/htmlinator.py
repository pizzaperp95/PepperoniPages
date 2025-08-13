# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages HTMLinator Version 0.1
# Turns the file into HTML, then inserts it into the template.

import sys
import markdown
import os

tempfile = "../temp/file.temp"
filename = tempfile
debugMode = False
openedfile = []
template = sys.argv[1]
htmlsource = ""
templatefile = []

def striplines(_filetostrip):
    returnvalue = []
    # Turn the file into an array, where each element of that array is one line of the file.
    with open(_filetostrip, 'r', encoding='UTF-8') as file:
        returnvalue = [line.rstrip('\n') for line in file]
    if debugMode: 
        print(returnvalue)
    return returnvalue

def tohtml():
    global htmlsource
    with open(filename, 'r') as file:
        filecontent = file.read()
    htmlsource = markdown.markdown(filecontent, extensions=['tables'])
    if debugMode: print(htmlsource)

    for i, val in enumerate(templatefile):
        if len(val) > 0:
            if (val.strip().lower() == "<pepperonipages>"):
                templatefile[i] = htmlsource
    htmlsource = '\n'.join(templatefile)


def loadTemplate():
    global templatefile
    os.chdir('../templates')
    templatefile = striplines(template)

def finish():
    with open(tempfile, 'w', encoding='UTF-8') as file:
        file.write(htmlsource)

def main():
    global openedfile
    openedfile = striplines(tempfile)
    loadTemplate()
    tohtml()
    finish()

if __name__=="__main__":
    main()