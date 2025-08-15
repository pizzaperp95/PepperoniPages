# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages P2F Parser Version 0.1
# Strips everything out except for everything inside mdstart-mdend.

import sys

def str_to_bool(str):
    if (str.upper() == "TRUE"):
        return True
    else:
        return False

debugMode = str_to_bool(sys.argv[2])

tempfile = "../temp/file.temp"
filename = tempfile
openedfile = []

def striplines():
    global openedfile
    # Turn the file into an array, where each element of that array is one line of the file.
    with open(filename, 'r+', encoding='UTF-8') as file:
        openedfile = [line.rstrip('\n') for line in file]

def parse(_contents):
    pass

def stripAllBeforeMDstart():
    for i, val in enumerate(openedfile):
        if val.upper() == "MDSTART":
            break
        else:
            openedfile.pop(i)

# Strips out mdstart and mdend from file. 
def stripMdTags(): # (and P2FORMATVER cuz i dont wanna rename this function)
    global openedfile
    #openedfile = [item for item in openedfile if item.upper() != "MDSTART"]
    for i, val in enumerate(openedfile):
        if val.upper() == "MDSTART" or val.upper() == "MDEND" or (val.upper().split("=")[0]) == "P2FORMATVER":
            openedfile.pop(i)

# Main function, duh.
def main():
    striplines()
    stripAllBeforeMDstart()
    stripMdTags()
    finishParsing()

def finishParsing():
    with open(tempfile, 'w', encoding='UTF-8') as file:
        
        for items in openedfile:
            file.write('%s\n' %items)
    print("Parsing finished successfully.")
    for i in range(len(openedfile)):
        print(openedfile[i])


if __name__=="__main__":
    main()


