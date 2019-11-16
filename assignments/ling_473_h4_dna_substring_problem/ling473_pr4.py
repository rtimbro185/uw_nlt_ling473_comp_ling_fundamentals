import os
import fnmatch
import mmap
import contextlib
from collections import defaultdict
import codecs

isLocal = True
markers = defaultdict(list)
#BUF_SIZE = 100000
#MAX_TARGET_LEN = 5000
######################################
# Main Procedural Function
######################################
def main():
   
    fileCount = 0
    corpusPath = None
    dnaFileNames = []
    trie = [[]]
    extraCredit = "./extra-credit"
    
    #Genome DNA Corpus Data
    if isLocal: corpusPath = "./genome/corpus_dna/"
    else: corpusPath = "/opt/dropbox/16-17/473/project4/hg19-GRCh37"
    
    #Genome DNA Target sequences
    if isLocal: fileTargetsName = "./genome/targets"
    else: fileTargetsName = "/opt/dropbox/16-17/473/project4/targets"
   
    output = codecs.open("output.txt",encoding='utf-8', mode='w')
    
   
    try:
        #Load the target sequences into trie data structure
        targets = loadTargetSequences(fileTargetsName, trie)
        
        #Find all of the DNA files to process
        for dirpath, dirs, files in os.walk(corpusPath):
            for filename in fnmatch.filter(files, '*.dna'):
                dnaFileNames.append(dirpath+'/'+filename)
                
        #an iterable list of DNA files to process
        for dnaFile in dnaFileNames:
            process(trie,dnaFile,output)
        
        #Extra credit
        printTargetGrouping(extraCredit)
        
    except Exception as e:
        print(e)
    
    output.flush()
    output.close()


##################################################################################################################
# The loadTargetSequences function... returns a trie data structure populated with target sequences
##################################################################################################################
def loadTargetSequences(file, tr):
    
    with open(file) as f:
        for line in f:
            insertKey(line[:-1], [], tr)
        
    f.close()
    
    
##################################################################################################################
# The process function...
##################################################################################################################
def process(trie, dnafile,output):
    print("%s"%dnafile)
    output.write("%s"%dnafile)
    Ci = 0
    Cj = 0
    remaining = 0
    
    with codecs.open(dnafile, encoding='utf-8', mode='rb') as f:
    #with open(dnafile, 'rb') as f:
        m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        remaining = m.size()
        mSize = m.size()
        Cj = Ci
        while Ci < mSize:
            print(m[Ci:Cj+1])
            print("Remaining -->%d"%remaining)
            prefix = normalizePrefixSearch(m[Ci:Cj+1])
            if prefix != None: 
                br = retrieveBranch(prefix,trie)
                if br != None:
                    if isTrieBucket(getChildBranches(br)[0]):
                        #found key target
                        bucket = br[1]
                        bucketKey = bucket[0]
                        markers[m[Ci:Cj+1].decode()].append((hex(Ci),dnafile))
                        print("%s\t%s"%(hex(Ci),m[Ci:Cj+1].decode()))
                        output.write("%s\t%s"%(hex(Ci),m[Ci:Cj+1].decode()))
                        Ci+=1; remaining-=1
                        Cj = Ci
                    else:
                        #not a terminal node, move forward one without advancing the corpus character
                        Cj+=1; continue
                else:
                    Ci+=1; remaining-=1
                    Cj = Ci
            else:
                Cj+=1
                Ci+=1; remaining-=1
                
        m.close()
    f.close()
    output.flush()
           

##################################################################################################################
# The readTargets function accepts a file name as input and returns an array of targets contained within the file
##################################################################################################################   
def readTargets(file):
    targets = []
    
    with open(file) as f:
        for line in f:
            targets.append(line)
    
    f.close() 
    return targets

##################################################################################################################
# Insert Trie Keys
##################################################################################################################
def insertKey(k,v,trie):
    #don't insert empty key
    if k == '':
        return None
    #if trie has key or stores it with the same value v, do not insert
    elif hasKey(k,trie) and retrieveValue(k,trie) == v:
         return None
    else:
        tr = trie
        #for each character c in k, find a child branch that starts with c
        for c in k:
            br = findChildBranch(tr,c)
            #if there is no branch that starts with c, create it and append it at the end of the current level
            if br == None:
                newBr = [c]
                tr.append(newBr)
                tr = newBr
            else:
                tr = br
        #tr is now bound to the branch, insert a new bucket
        tr.append((k,[v]))
        return None

##################################################################################################################
# Helper Functions
##################################################################################################################
def getBucketValue(b):
    return b[1][0]

def setBucketValue(b,v):
    bucketValue = b[1][0]
    bucketValue.append(v)

def getBucketKey(b):
    return b[0]

def isTrieBranch(x):
    return isinstance(x,list)

def isTrieBucket(x):
    return isinstance(x, tuple) and \
        len(x) == 2 and \
        isinstance(x[0], str) and \
        isinstance(x[1], list) and \
        len(x[1]) == 1

#a branch is either empty or it is a list whose first element is a character
#and the rest are buckets or sub-branches
def getChildBranches(trie):
    if trie == []:
        return []
    else:
        return trie[1:]

#Searches for a child branch of the trie where the branches first character equals c
def findChildBranch(trie,c):
    for br in getChildBranches(trie):
        if br[0] == c:
            return br
    return None
    
#RETRIEVE_VALUE, find a branch in trie that is indexed under k
def retrieveBranch(k,trie):
    if k == '':
        return None
    else:
        tr = trie
        for c in k:
            br = findChildBranch(tr,c)
            if br == None:
                return None
            else:
                tr = br
        return tr
    
#RETRIEVE_VALUE, return the bucket value of the branch specified by the key input parameter - k
def retrieveValue(k,trie):
    if not hasKey(k,trie): return None
    br = retrieveBranch(k,trie)
    return getBucketValue(br[1])

#HAS_KEY, returns True if trie has the key passed in as a parameter, false otherwise
def hasKey(k,trie):
    br = retrieveBranch(k,trie)
    if br == None:
        return False
    else:
        return isTrieBucket(getChildBranches(br)[0])

##################################################################################################################
# The indexDNABases function accepts a byte character and returns an integer representation for that input
##################################################################################################################
def indexDNABases(ch):

    if chr(ch) == 'a' or chr(ch) == 'A':
        return 65 #'A'
    elif chr(ch) == 'c' or chr(ch) == 'C':
        return 67 #'C'
    elif chr(ch) == 'g' or chr(ch) == 'G':
        return 71 #'G'
    elif chr(ch) == 't' or chr(ch) == 'T':
        return 84 #'T'
    else:
        return -1

#Normalize Search Prefix
def normalizePrefixSearch(prefix):    
    norms = bytearray()
    for p in prefix:
        #break if prefix character not one of base nucliotides A, C, G, T
        if indexDNABases(p) == -1: return None
        norms.append(indexDNABases(p))  
    prefix = norms.decode()
    return prefix

#Extra credit, print, groupby target
def printTargetGrouping(file):
    
    f = open(file,'w')
    for target in markers:
        f.write(target[0]+"\t"+target[1]+"\n")
    
    f.flush()
    f.close()
    

    
    
##################################################################################################################
# Start With Prefix
# 1.) Find the branch indexed by prefix
# 2.) Go through the sub-branches of the branch indexed by the prefix and collect the bucket strings into keyList
##################################################################################################################
def startWithPrefix(prefix,trie,v):
    norms = bytearray()
    for p in prefix:
        #break if prefix character not one of base nucliotides A, C, G, T
        if indexDNABases(p) == -1: return []
        norms.append(indexDNABases(p))
        
    prefix = norms.decode()
    
    br = retrieveBranch(prefix,trie)
    if br == None: return []
    
    keyList = []
    q = getChildBranches(br)
    
    while not q == []:
        currBr = q.pop()
        if isTrieBucket(currBr):
            keyList.append(getBucketKey(currBr))
        elif isTrieBranch(currBr):
            q.extend(getChildBranches(currBr))
        else: return 'ERROR: bad branch'
    return keyList
##################################################################################################################
# Execute Main Function
##################################################################################################################
if __name__ == "__main__": main()