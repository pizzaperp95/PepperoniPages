# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages Version 0.1
# Gets the P2Format Version and starts the other processes.

import sys
import os
import shutil
import subprocess
from pathlib import Path

filename = sys.argv[1]
p2formatver = 0
openedfile = []
template = ""
tempfile = "../temp/file.temp"
debugMode = True
fileexportpath = Path("./")

# Main function
def main():
    os.chdir('../pages')
    setFileOutput()
    if not (os.path.exists("../temp")): os.mkdir("../temp")

    if (os.path.exists(tempfile)):
        os.remove(tempfile)
    path = shutil.copy(filename,tempfile)
    striplines(filename)
    getp2fver()
    getTemplate()

    subprocess.run(["python", "../source/preprocessor.py", filename])
    subprocess.run(["python", "../source/parse.py", filename])
    finish()
            
def getp2fver():
    global p2formatver
    global openedfile
    # Turn the file into an array, where each element of that array is one line of the file.
    for i, val in enumerate(openedfile):
        if len(val) > 0:
            line = val.split('=')
            if (line[0].upper() == "P2FORMATVER"):
                p2formatver = line[1]
                #openedfile.pop(i)
                if debugMode: print("P2Format Version set to:", p2formatver)

def getTemplate():
    global openedfile
    global template

    for i, val in enumerate(openedfile):
        if len(val) > 0:
            line = val.split('=')
            if (line[0] == "template"):
                p2formatver = line[1]
                openedfile.pop(i)
                if debugMode: print("Template:", p2formatver)

def striplines(file):
    global openedfile
    # Turn the file into an array, where each element of that array is one line of the file.
    with open(file, 'r+', encoding='UTF-8') as file:
        openedfile = [line.rstrip('\n') for line in file]
    if debugMode: 
        print(openedfile)

def setFileOutput():
    global fileexportpath
    pathtemp = Path(filename)
    path = Path(pathtemp.parent) / (pathtemp.stem + ".html")
    fileexportpath = os.path.join("../out", path)
    fileexportpath = Path(fileexportpath)
    print(fileexportpath)

def finish():
    striplines(tempfile)
    global fileexportpath
    fileexportpath.parent.mkdir(exist_ok=True, parents=True)
    path = shutil.copy("../temp/file.temp", fileexportpath)
        

    if debugMode: return
    try:
        shutil.rmtree('../temp')
    except OSError as e:
        print(f"error: {e.filename} - {e.strerror}.")


if __name__=="__main__":
    main()
