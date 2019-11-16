#!/opt/python-3.4/bin/python3.4
#  -*- coding: utf-8 -*-

#Author: Ryan Timbrook
#Date: 9/8/16
#Project: Ling 473 Project 5

import os, fnmatch, codecs, sys, re
from collections import defaultdict
from classifier import LMFrequencyDist
from classifier import TextProbDist

###    Globals
isLocal = True
isTrain = False

#    CONSTANTS
ENCODING = "latin_1"
MODE_READ_BINARY = "rb"
MODE_WRITE = "w"
FILE_SUFFIX = ".unigram-lm"
PUNCT = ('''.,!¡¥$£?¿;:()"—–-/[]¹²³«»''')
INPUT_TEST = "test.txt"
INPUT_TRAIN = "train.txt"
INPUT_EXTRA_TEST = "extra-test.txt"
INPUT_EXTRA_TRAIN = "extra-train.txt"

LOCAL_PATH = "./fromPatas/"
REMOTE_PATH = "/opt/dropbox/16-17/473/project5/"

#######################################################################################
# Main Procedural Function
#######################################################################################
def main():
    #Data to analyze
    if isLocal: 
        path = LOCAL_PATH; file = LOCAL_PATH + INPUT_TEST
    else: 
        path = REMOTE_PATH+"language-models"; file = REMOTE_PATH + INPUT_TEST
    
    if isTrain: file = LOCAL_PATH + INPUT_TRAIN
   
    
    #Run a preprocessing step and load the language model words
    allWords = preProcess(path)
    exampleText = getTestExamples(file)
    
    #process each example from input
    for example in exampleText:
        process(example,allWords)

#######################################################################################
# Core process function
#######################################################################################
def process(doc,words):
    #calculate the entire, 15 language sample space size. Use this tally in calculating smoothing of none found words
    tots = []
    for l in words: tots.append(l.N())
    allLmWordCount = sum(tots)
    #repeat calculations for each of the 15 language models
    for lm in words:
        wordMatchCount = 0
        #print("language --> {0}".format(lm.getLangId()))
        lmP, wc, tc, wP, sz = float(0), float(0), float(0), float(0), float(0)
        tc = lm.N()
        sz = lm._le_()
        sz = float(sz)
        
        for word in doc.textFragments():
            wordCount = len(doc.textFragments())
            if word in lm.keys():
                try:
                    wordMatchCount+=1
                    idx = lm.keyIndex(word)
                    #print("word found --> {0}, at index --> {1}".format(word,idx))
                    #print("word count --> {0}, at index --> {1}".format(lm.keyValue(int(idx)),idx))
                    wc = lm.wordCount(int(idx))
                    #lmP = wc / tc
                    lmP = doc.prob(wc,tc)
                except KeyError as ke:
                    print("Caught Key Error --> {0} at word '{1}', word idx {2}".format(ke,word,idx))
                    #if a word isn't found, assume it's a singleton of the entire 15 language samples space (91,373,647)
                    lmP = doc.smooth(allLmWordCount)
                    pass
            else:
                #if a word isn't found, assume it's a singleton of the entire 15 language samples space (91,373,647)
                lmP = doc.smooth(allLmWordCount)
            doc.setWordProbabilities(word,lmP)
        
        #calculate all probabilities
        try:
            wP = doc.logprob()
        except ValueError:
           pass 
        doc.setLanguageProbabilities(lm.getLangId(),wP)
        #clean VO collection
        doc.wordProbabilities = {}
        
    #calculate argmax
    doc.max()
    #print this documents results for the 15 sentences
    doc.printOutput()
    
    #clean VO collection
    doc.setLanguageProbabilities = {}   
 
#######################################################################################
# Function: preProcess, Read in all of the language model counts
#######################################################################################
def preProcess(path):
    lmFreqDistros = []
    
    lms = getFilesFromPath(path)
    for files in lms:
        for lang, file in files.items():
            lmFreqDist = LMFrequencyDist(lang)
            with codecs.open(file,encoding=ENCODING,mode='r',errors='strict') as f:
                lines = f.readlines()
                for line in lines:
                    line = line[:-1]
                    word = line.split('\t')[0]
                    count = line.split('\t')[1]
                    lmFreqDist.setWordCounts((word,int(count)))
            lmFreqDist.utilCreateWordMaps()
            lmFreqDistros.append(lmFreqDist)
  
    return lmFreqDistros
                
##################################################################################################################
# File IO - Helper Functions - Gets the Language Model file locations
##################################################################################################################
def getFilesFromPath(path):
    langMap = {}
    langModels = []
    
    for dirpath, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, "*"+FILE_SUFFIX):
            langModels.append({filename.split('.')[0]:dirpath+'/'+filename})
    
    return langModels    

##################################################################################################################
# File IO - Helper Functions - Gets the Test Example words
##################################################################################################################
def getTestExamples(file):
    examples = []
    
    with codecs.open(file,encoding=ENCODING,mode='r') as f:
        sentences = f.readlines()
        for sent in sentences:
            wm = removePunctuation(sent[:-1])
            examples.append(TextProbDist(wm[0],sent.split('\t')[1][:-1],wm[1]))
        
    return examples

##################################################################################################################
# Helper Functions - Remove punctuation
##################################################################################################################
def removePunctuation(sent):
    identifier = sent.split('\t')[0]
    text = sent.split('\t')[1]
    tokens = text.split()
   
    words = []
    
    for token in tokens:
        newChars = []
        for chr in token:
            if chr in PUNCT:
                newChars.append('')
            else:
                newChars.append(chr)
                
        words.append(''.join(newChars))
    return identifier,words

##################################################################################################################
# Execute Main Function
##################################################################################################################
if __name__ == "__main__": main()