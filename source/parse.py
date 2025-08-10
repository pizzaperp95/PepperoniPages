# (c) 2025 Pizza https://pizza.syntropicinteractive.com/
# This code is licensed under MIT license (see LICENSE.txt for details)
# Pepperoni Pages P2F Parser Version 0.1
# Strips everything out except for everything inside mdstart-mdend.

import sys

filename = sys.argv[1]

def stripComments(_contents):
    pass

def parse(_contents):
    pass


# Main function, duh.
def main():
    with open(filename) as file:
        while line := file.readline():
            print(line.rstrip())


if __name__=="__main__":
    main()


