#!/opt/python-3.4/bin/python3.4

#Author: Ryan Timbrook
#Date: 9/10/16
#Project: Ling 473 Project 6 (Optional Extra Credit)

import os, fnmatch, codecs, sys, re
from collections import defaultdict
import distance

###    Globals
isLocal = False
isGagaValidation = False

#    CONSTANTS
ENCODING = "cp1252"
MODE_READ = "r"
MODE_WRITE = "w"
INPUT_BP_1 = "bp-20100419.txt"
INPUT_BP_2 = "bp-20100828.txt"
INPUT_GAGA_1 = "gaga0.txt"
INPUT_GAGA_2 = "gaga1.txt"

LOCAL_PATH = "./input/"
REMOTE_PATH = "/opt/dropbox/16-17/473/project6/"

#######################################################################################
# Main Procedural Function
#######################################################################################
def main():
    #Data to analyze
    path = REMOTE_PATH
    if isLocal: path = LOCAL_PATH
    
    if not isGagaValidation:
        file1 = path+INPUT_BP_1; file2 = path+INPUT_BP_2
    else:
        file1 = path+INPUT_GAGA_1; file2 = path+INPUT_GAGA_2
    
    texts = getText(file1, file2)
 
    ed = distance.EditDistance(texts[1],texts[0],"sent")
    ed.alignText(ed.n, ed.m)
    ed.bestAlignment = list(reversed(ed.bestAlignment))
    ed.printEditDistance()
    ed.printAlignment()


##################################################################################################################
# File IO - Helper Functions - Gets the Test Example words
##################################################################################################################
def getText(preText,postText):
    
    priorArticalText = []
    afterArticalText = []
    
    with codecs.open(preText,encoding=ENCODING,mode='r') as f:
        [[priorArticalText.append(line[:-1])] for line in f.readlines()]
        
    with codecs.open(postText,encoding=ENCODING,mode='r') as f:
        [[afterArticalText.append(line[:-1])] for line in f.readlines()]
        
    return priorArticalText, afterArticalText

##################################################################################################################
# Execute Main Function
##################################################################################################################
if __name__ == "__main__": main()