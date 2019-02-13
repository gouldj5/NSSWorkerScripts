# $language = "Python"
# $interface = "1.0"

# This script shows how to read in a file, and it demonstrates how to
# perform some preprocessing on data (splitting the file data into
# separate strings) before sending it to a server.

import os

def main():
    crt.Screen.Synchronous = True

    for line in open("C:\\Users\\josht_sh96rlx\\OneDrive - Rowan University\\NSSWorkerScripts\\set.txt", "r"):
        # Send the line with an appended CR
        #

        crt.Screen.Send(line + '\r')

        # Wait for my prompt before sending the next line
        #
        crt.Screen.WaitForString("#")

    crt.Screen.Synchronous = False


main()
