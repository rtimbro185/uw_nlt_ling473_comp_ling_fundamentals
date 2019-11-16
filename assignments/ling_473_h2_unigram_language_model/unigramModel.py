

import os
import fnmatch
import re
from collections import defaultdict

######################################
# Main Procedural Function
######################################
def main():
    #Data paths
    corpusPath = "/corpora/LDC/LDC02T31/nyt/2000"
    
    fileCount = 0
    wordCount = 0
    words = []
    wordDict = defaultdict()
    
    #Find and open all data files for analysis
    for dirpath, dirs, files in os.walk(corpusPath):
        for filename in fnmatch.filter(files, '*_NYT'):
            with open(os.path.join(dirpath, filename)):
                fileCount += 1
                rawFile = open(dirpath+'/'+filename)
                
                #Clean file, return character array
                words = cleanNonWordChars(cleanTagsAndFlatten(rawFile))
                wordCount = wordCount + len(words)
                #Tally number of instances of each word.
                for word in sorted(words):
                    if word not in wordDict: wordDict[word] = 1; continue
                    wordDict[word] += 1
   
    #Sort the words by frequency in descending order and print the result out to the console
    wordDict = sorted(wordDict.items(),key=lambda x:x[1],reverse=True)
    for wordFreq in wordDict:
        print('%s \t %d'%(wordFreq[0],wordFreq[1]))
    
    

##################################################################################################################
# Function: Utility function to clean the document of all SGML tags, replacing them with an empty string
##################################################################################################################
def cleanTagsAndFlatten(doc):
    docLines=[]
    
    #Create a pattern which identifies all tags in the document
    tagsPattern = re.compile(r'<.*?>')
    for line in doc:
        line = re.sub(r'\n',' ',line)
        cleaned = tagsPattern.sub('',line)
        words = cleaned.split(' ')
        
        for word in words:
            if word == '\n': word = ' '
            if word != '': docLines.append(word)
    
    return ' '.join(docLines)

##################################################################################################################
# Function: Utility function to clean the document of all non words (i.e. punctuation, symbols, digits)
##################################################################################################################
def cleanNonWordChars(doc):
    docWords = []
    #Remove non-words
    doc = re.sub(r"([a-zA-Z]+[0-9]+)|([0-9]+[a-zA-Z]+)|(&[a-zA-Z]+)|(\w+(-\w+)+)|([a-zA-Z])(\.[a-zA-Z])+\.?",'',doc)
   
    #Create pattern to extract words with apostrophies
    wordsPatternWithApostrophe = re.compile(r"[a-zA-Z]+'?[a-zA-Z]+")
    words = re.findall(wordsPatternWithApostrophe, doc)
    
    #Convert all words to lowercase
    docWords = [x.lower() for x in words]
    return docWords

##################################################################################################################
# Execute Main Function
##################################################################################################################
if __name__ == "__main__": main()