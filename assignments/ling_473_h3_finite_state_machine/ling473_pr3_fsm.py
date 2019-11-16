#  -*- coding: utf-8 -*-

#Author: Ryan Timbrook
#Date: August 23, 2016
#Project: Ling 473, Project 3


import codecs
from collections import defaultdict

#GLOBAL - > Thai character unicode values
#Globals

V1 = u"\u0E40\u0E41\u0E42\u0E43\u0E44"
C1 = u"\u0E01\u0E02\u0E03\u0E04\u0E05\u0E06\u0E07\u0E08\u0E09\u0E0A\u0E0B\u0E0C\u0E0D\u0E0E\u0E0F" \
     + u"\u0E10\u0E11\u0E12\u0E13\u0E14\u0E15\u0E16\u0E17\u0E18\u0E19\u0E1A\u0E1B\u0E1C\u0E1D\u0E1E\u0E1F" \
     + u"\u0E20\u0E21\u0E22\u0E23\u0E24\u0E25\u0E26\u0E27\u0E28\u0E29\u0E2A\u0E2B\u0E2C\u0E2D\u0E2E"
C2 = u"\u0E23\u0E25\u0E27\u0E19\u0E21"
V2 = u"\u0E34\u0E35\u0E36\u0E37\u0E38\u0E39\u0E31\u0E47"
T  = u"\u0E48\u0E49\u0E4A\u0E4B"
V3 = u"\u0E32\u0E2D\u0E22\u0E27"
C3 = u"\u0E07\u0E19\u0E21\u0E14\u0E1A\u0E01\u0E22\u0E27"

######################################
# Main Procedural Function
######################################
def main():
    #Input / Output Files
    docUtf8Name = "./fsm-input.utf8.txt"
    outputFileName = "./timbrr.html"
    
    #Load Thai input document
    thaiDoc = codecs.open(docUtf8Name, encoding='utf-8')

    #Open output file for writing
    outputFile = codecs.open(outputFileName, encoding='utf-8', mode='w')
    outputFile.write(u"<html><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><body>")
    
    docLineCount = 0
    for line in thaiDoc.readlines():
        docLineCount += 1
        
        result = finiteStateTransducer(line[:-1])
        
        outputFile.write(result+ u"<br/>")
        
    outputFile.write(u"</body></html>")
    
    #outputFile.flush()
    outputFile.close()

##################################################################################################################
# Finite State Transducer; Transform the input to the result
# Description: For states 0 through 9, echo the input character to the output. States 7,8, and 9 are the cases
#                 where a syllable break has been detected.
##################################################################################################################
def finiteStateTransducer(input):
    state = 0;
    formatedInput = ''
    tempChars = []
    wordranges = defaultdict(list)
    wordCount = 1
    wordranges[wordCount] = [{"startWordRange":0},{"endWordRange":0}]
    
    for i, e in enumerate(input):
        #Action, Accept V1 and C1
        if state == 0:
            if e in V1: state = 1
            elif e in C1: state = 2
            else: raise Exception
            
        #Action, Accept C1
        elif state == 1:
            if e in C1:  state = 2
            else: raise Exception
            
        #Action, Accept C2/V2/T/V3/C3/V1/C1
        elif state == 2: 
            if e in C2: state = 3
            elif e in V2: state = 4
            elif e in T: state = 5
            elif e in V3: state = 6
            elif e in C3: state = 9
            elif e in V1: 
                if i == len(input)-1: break
                else: state = 7
            elif e in C1: 
                if i == len(input)-1: break
                else: state = 8
            else: raise Exception
            
        #Action, Accept V2/T/V3/C3
        elif state == 3:
            if e in V2: state = 4
            elif e in T: state = 5
            elif e in V3: state = 6
            elif e in C3: state = 9
            else: raise Exception
            
        #Action, Accept T/V3/C3/V1/C1
        elif state == 4:
            if e in T: state = 5
            elif e in V3: state = 6
            elif e in C3: state = 9
            elif e in V1: 
                if i == len(input)-1: break
                else: state = 7
            elif e in C1: 
                if i == len(input)-1: break
                else: state = 8
            else: raise Exception
            
        #Action, Accept V3/C3/V1/C1
        elif state == 5:
            if e in V3: state = 6
            elif e in C3: state = 9
            elif e in V1: 
                if i == len(input)-1: break
                else: state = 7
            elif e in C1: 
                if i == len(input)-1: break
                else: state = 8
            else: raise Exception
            
        #Action, Accept C3/V1/C1
        elif state == 6:
           
            if e in C3: state = 9
            elif e in V1: 
                if i == len(input)-1: break
                else: state = 7
            elif e in C1: 
                if i == len(input)-1: break
                else: state = 8
            else: raise Exception
            
        #Action, Break before previous character, Transition to state 1
        if state == 7:
            wordranges[wordCount][1]["endWordRange"] = i-1
            wordranges[wordCount+1] = [{"startWordRange":i},{"endWordRange":0}]
            
            start = wordranges[wordCount][0]["startWordRange"]
            stop = wordranges[wordCount][1]["endWordRange"]
            
            formatedInput = formatedInput + input[start:stop+1]+u" "
    
            state = 1
            wordCount +=1
            continue
        #Action, Break before previous character, Transition to state 2
        if state == 8:
            wordranges[wordCount][1]["endWordRange"] = i-1
            wordranges[wordCount+1] = [{"startWordRange":i},{"endWordRange":0}]
            
            start = wordranges[wordCount][0]["startWordRange"]
            stop = wordranges[wordCount][1]["endWordRange"]
            
            formatedInput = formatedInput + input[start:stop+1]+u" "
            
            wordCount +=1
            state = 2
            
            continue
        #Action, Break now, Transition to state 0
        if state == 9:
            wordranges[wordCount][1]["endWordRange"] = i-1
            wordranges[wordCount+1] = [{"startWordRange":i+1},{"endWordRange":0}]
            
            start = wordranges[wordCount][0]["startWordRange"]
            stop = wordranges[wordCount][1]["endWordRange"]
            
            formatedInput = formatedInput + input[start:stop+2]+u" "
            
            wordCount +=1
            state = 0
            continue
        
    #Capture final word
    if len(input) > wordranges[wordCount][0]["startWordRange"]:
        formatedInput = formatedInput + input[wordranges[wordCount][0]["startWordRange"]:len(input)]
    
   
    return formatedInput.strip()
   

##################################################################################################################
# Execute Main Function
##################################################################################################################
if __name__ == "__main__": main()
