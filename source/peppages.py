# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages Version 0.1
# Gets the P2Format Version and starts the other processes.

import sys
import os
import shutil
import subprocess

filename = sys.argv[1]
p2formatver = 0
debugMode = True

# Main function
def main():
    if not (os.path.exists("./temp")): os.mkdir("./temp")

    path = shutil.copy(filename,"./temp/file.temp")
    getp2fver()
    subprocess.run(["python", "preprocessor.py", filename])
            
def getp2fver():
    # Turn the file into an array, where each element of that array is one line of the file.
    with open(filename, 'r', encoding='UTF-8') as file:
        openedfile = [line.rstrip('\n') for line in file]  
        for i, val in enumerate(openedfile):
            if len(val) > 0:
                line = val.split('=')
                if (line[0] == "P2FORMATVER"):
                    p2formatver = line[1]
                    if debugMode: print("P2Format Version set to:", p2formatver)


if __name__=="__main__":
    main()
