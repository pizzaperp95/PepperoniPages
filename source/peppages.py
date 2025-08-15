# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages Version 0.2
# Gets the P2Format Version and starts the other processes.

import sys
import os
import shutil
import subprocess
from pathlib import Path
from enum import Enum

filename = ""
p2formatver = 0
openedfile = []
template = ""
tempfile = "../temp/file.temp"
debugMode = False
fileexportpath = Path("./")
batchpath = ""

class mode(Enum):
    SINGLE = 0
    BATCH = 1

ppagesMode = mode.SINGLE

# Main function
def main():
    global template
    global filename

    handleArgs()

    os.chdir('../pages')
    if ppagesMode == mode.BATCH:
        file_path = Path(batchpath)
    
        for f in file_path.rglob('*.p2f'): 
            filename = f
            pepperoniPages()
    elif ppagesMode == mode.SINGLE:
        pepperoniPages()

            
def getp2fver():
    global p2formatver
    global openedfile
    # Turn the file into an array, where each element of that array is one line of the file.
    for i, val in enumerate(openedfile):
        if len(val) > 0:
            line = val.split('=')
            if (line[0].upper() == "P2FORMATVER"):
                p2formatver = line[1]
                openedfile.pop(i)
                if debugMode: print("P2Format Version set to:", p2formatver)

def pepperoniPages():
    global template
    global filename

    setFileOutput()
    if not (os.path.exists("../temp")): os.mkdir("../temp")

    if (os.path.exists(tempfile)):
        os.remove(tempfile)
    path = shutil.copy(filename,tempfile)

    striplines(filename)
    getp2fver()
    getTemplate()

    subprocess.run(["python", "../source/preprocessor.py", filename, debugMode])
    subprocess.run(["python", "../source/parse.py", filename, debugMode])
    subprocess.run(["python", "../source/htmlinator.py", template, debugMode])
    finish()


def getTemplate():
    global openedfile
    global template

    for i, val in enumerate(openedfile):
        if len(val) > 0:
            line = val.split('=')
            if (line[0] == "template"):
                template = line[1]
                #openedfile.pop(i)
                if debugMode: print("Template:", template)

def striplines(file):
    global openedfile
    # Turn the file into an array, where each element of that array is one line of the file.
    with open(file, 'r+', encoding='UTF-8') as file:
        openedfile = [line.rstrip('\n') for line in file]

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
    if (os.path.exists(fileexportpath)):
        os.remove(fileexportpath)
    path = shutil.copy("../temp/file.temp", fileexportpath)
        

    if debugMode: return
    try:
        shutil.rmtree('../temp')
    except OSError as e:
        print(f"error: {e.filename} - {e.strerror}.")

def handleArgs(): # Arrgg!!! (yes theres much better ways of handling arguments, but this is good enough for now.)
    global ppagesMode
    global  batchpath
    global filename

    if 2 > len(sys.argv):
        print("ERROR: No first argument supplied!")
        exit()

    if 3 > len(sys.argv):
        print("ERROR: No second argument supplied!")
        exit()

    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = ""
    if not (4 > len(sys.argv)):
        arg3 = sys.argv[3]

    match  arg1:
        case "-batch":
            ppagesMode = mode.BATCH
        case "-b":
            ppagesMode = mode.BATCH
        case "-single":
            ppagesMode = mode.SINGLE
        case "-s":
            ppagesMode = mode.SINGLE
        case _:
            print("ERROR: invalid first argument!")
            sys.exit()

    batchpath = arg2
    filename = arg2

    if (arg3.upper == "-debug"):
        debugMode = True
    


                
              

if __name__=="__main__":
    main()
