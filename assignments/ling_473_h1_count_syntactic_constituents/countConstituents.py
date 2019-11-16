#Author: Ryan Timbrook
#Date: August 4, 2016
#Project: Ling 473, Project 1

import os
import fnmatch
import re
import string
import numpy as np

isTest = False
isLocalTest = False

######################################
# Main Procedural Function
######################################
def main():
    
    if isLocalTest:
        corpusPath = "./test/"
    else:
        corpusPath = "/corpora/LDC/LDC99T42/RAW/parsed/prd/wsj/14"
    
    summaryTable = {'S':0,'NP':0,'VP':0,'DVP':0,'IVP':0}
    
    #test, sample corpus data
    for dirpath, dirs, files in os.walk(corpusPath):
        for filename in fnmatch.filter(files, '*.prd'):
            with open(os.path.join(dirpath, filename)):
                
                #Clean file, return character array
                docChars = utilCharacterArray(open(dirpath+'/'+filename))
               
                #Get Counts from file
                summaryTable['S'] += getSentenceCount(docChars)
                summaryTable['NP'] += getNounPhraseCount(docChars)
                summaryTable['VP'] += getVerbPhraseCount(docChars)
                summaryTable['DVP'] += getDitransitiveVerbPhraseCount(docChars)
                summaryTable['IVP'] += getIntransitiveVerbPhraseCount(docChars)
                
    #Print's final Count output to stdout
    print("Constituent Counts: \n Sentence Count = %d \n Noun Phrase Count = %d \n Verb Phrase Count = %d \n Ditransitive Verb Phrase = %d \n Intransitive Verb Phrase Count = %d"%(summaryTable['S'],summaryTable['NP'],summaryTable['VP'],summaryTable['DVP'],summaryTable['IVP']))

########################################################################
# Function: Get's Sentence Constituent Count, Pattern to Match (S ...)
########################################################################
def getSentenceCount(docChars):
    assert docChars != None;"Sentence, Character list can not be null!"
    sCount = 0
    sPattern = '(S'
     
    sCount = docChars.count(sPattern)
    
    return sCount
    
###########################################################################
# Function: Get's Noun Phrase Constituent Count, Pattern to Match (NP ...)
###########################################################################   
def getNounPhraseCount(docChars):
    assert docChars != None;"Noun Phrase, Character List can not be null!"
    npCount = 0
    npPattern = '(NP'
    
    npCount = docChars.count(npPattern)
    
    return npCount

############################################################################
# Function: Get's Verb Phrase Constituent Count, Pattern to Match (VP ...)
############################################################################
def getVerbPhraseCount(docChars):
    assert docChars != None;"Verb Phrase, Character List can not be null!"
    vpCount = 0
    vpPattern = '(VP'
    
    vpCount = docChars.count(vpPattern)
    
    return vpCount

##########################################################################################################
# Function: Get's Ditransitive Verb Phrase Constituent Count, Pattern to Match (VP verb (NP ...)(NP ...))
##########################################################################################################
def getDitransitiveVerbPhraseCount(docChars):
    assert docChars != None;"Ditransitive Verb Phrase, Character List can not be null!"
    dvpCount = 0
    
    values = np.array(docChars)
    vpIndexs = np.where(values == '(VP')[0]
    npIndexs = np.where(values == '(NP')[0]
    
    for vpIndex in vpIndexs:
        if list(docChars[vpIndex+1])[0] != '(':
            try:
                
                if docChars[npIndexs[vpIndex+2]] == '(NP' and docChars[npIndexs[vpIndex+3]] == '(NP' and list(docChars[vpIndex+4])[0] != '(':
                    dvpCount += 1
            except IndexError:
                pass
                
    return dvpCount

##########################################################################################################
# Function: Get's Itransitive Verb Phrase Constituent Count, Pattern to Match (VP verb)
##########################################################################################################
def getIntransitiveVerbPhraseCount(docChars):
    assert docChars != None;"Intransitive Verb Phrase, Character List can not be null!"
    ivpCount = 0
    
    values = np.array(docChars)
    vpIndexs = np.where(values == '(VP')[0]
    for vpIndex in vpIndexs:
        if list(docChars[vpIndex+1])[0] != '(':
            try:
                if (list(docChars[vpIndex+2])[0] == '(' and list(docChars[vpIndex+2])[1] == 'S') or (list(docChars[vpIndex+2])[0] == '.'):  
                    ivpCount += 1
            except IndexError:
                pass
            
    return ivpCount

##################################################################################################################
# Function: Utility function to clean the document of new lines and tab, replacing them with a single white space
##################################################################################################################
def utilCharacterArray(doc):
    docCharacters = []
    
    for line in doc.readlines():
        line = re.sub(r"[\n\t]","",line)
        lineChars = line.split(" ")
    
        for char in lineChars:
            if char != '': docCharacters.append(char)
            
    return docCharacters
    
    
if __name__ == "__main__": main()