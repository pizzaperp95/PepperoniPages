# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages HTMLinator Version 0.2
# Turns the file into HTML, then inserts it into the template.

import sys
import markdown
import os
import peplib

debugMode = peplib.str_to_bool(sys.argv[2])

tempfile = "../temp/file.temp"
filename = tempfile
openedfile = []
template = sys.argv[1]
htmlsource = ""
templatefile = []
pageTitle = None

def striplines(_filetostrip):
    return peplib.striplines(_filetostrip)
    

def tohtml():
    global pageTitle
    global htmlsource
    with open(filename, 'r') as file:
        filecontent = file.read()
    htmlsource = markdown.markdown(filecontent, extensions=['tables'])

    for i, val in enumerate(templatefile):
        if len(val) > 0:
            titlecheckstrip = val.strip()
            titleCheck = titlecheckstrip[:7]
            if ((titleCheck.lower() == "<title>")):
                if(pageTitle != None):
                    templatefile[i] = ("<title>{0}</title").format(pageTitle)
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

def getTitle():
    global pageTitle
    for i, val in enumerate(openedfile):
        split = val.split("=")
        if split[0].upper() == "TITLE":
            pageTitle = str(split[1])


def main():
    global openedfile
    openedfile = striplines(tempfile)
    loadTemplate()
    getTitle()
    tohtml()
    finish()

if __name__=="__main__":
    main()