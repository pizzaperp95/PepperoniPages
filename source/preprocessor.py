# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages P2F Pre-Processor Version 0.1
# Handles the preprocessor directives.

import sys

#p2fversion = sys.argv[2]
debugMode = False

tempfile = "../temp/file.temp"
openedfile = []
filename = tempfile



def striplines():
    global openedfile
    # Turn the file into an array, where each element of that array is one line of the file.
    with open(filename, 'r', encoding='UTF-8') as file:
        openedfile = [line.rstrip('\n') for line in file]
    if debugMode: 
        print(openedfile)

def include(line, arg0):
    global openedfile
    if debugMode:
        print("Include directive found at line: ", line)

    with open(arg0) as file:
        tempIncMD = [line.rstrip('\n') for line in file]

    openedfile.pop(line)
    index = line
    for item in tempIncMD:
        openedfile.insert(index, item)
        index += 1

def comment(line):
    global openedfile

    openedfile.pop(line)
    if debugMode:
        print("Comment found at line: ", line)

def parse():
    global openedfile
    striplines()
    for i, val in enumerate(openedfile):
        if len(val) > 0:
            if (val[0] == "?"):
                line = val.split()
                directiveprocessor(i, line[0], line[1])
    if debugMode:
        print()
        for i in range(len(openedfile)):
            print(openedfile[i])
    finishPreprocessing()
          
def directiveprocessor(line, directive, arg):
    match directive:
        case "?!":
            comment(line)
        case "?inc":
            include(line, arg)

def finishPreprocessing():
    global openedfile
    with open(tempfile, 'r+', encoding='UTF-8') as file:
        
        for items in openedfile:
            file.write('%s\n' %items)
        
        print("Preprocessing finished successfully.")
    
    file.close()

# Main function
def main():
    # wait.. if theres only one function here, then why don't we just have if __name__=="__main__": call this function instead..?
    parse()
            


if __name__=="__main__":
    main()