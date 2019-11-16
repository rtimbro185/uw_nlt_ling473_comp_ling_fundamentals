import os
import fnmatch
import mmap
import contextlib

isLocal = True
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
    
    #Genome DNA Corpus Data
    if isLocal: corpusPath = "./genome/corpus_dna/"
    else: corpusPath = "/opt/dropbox/16-17/473/project4/hg19-GRCh37"
    
    #Genome DNA Target sequences
    if isLocal: fileTargetsName = "./genome/targets"
    else: fileTargetsName = "/opt/dropbox/16-17/473/project4/targets"
   
    try:
        #Load the target sequences into trie data structure
        targets = loadTargetSequences(fileTargetsName, trie)
        
        #Find all of the DNA files to process
        for dirpath, dirs, files in os.walk(corpusPath):
            for filename in fnmatch.filter(files, '*.dna'):
                dnaFileNames.append(dirpath+'/'+filename)
                
        #an iterable list of DNA files to process
        args = iter(dnaFileNames)
        
        process(trie, args.__next__(),targets)
        
        while args.__length_hint__() > 0:
            print("DNA File Iteration: %d"%args.__length_hint__())
            process(trie,args.__next__(),targets)
            
                   
    except Exception as e:
        print(e)


##################################################################################################################
# The loadTargetSequences function... returns a trie data structure populated with target sequences
##################################################################################################################
def loadTargetSequences(file, tr):
    print("loadTargetSequences: file %s"%file)
    targets = []
    count = 0
    with open(file) as f:
        for line in f:
            count += 1
            #print("Target Sequence Length [%d]"%len(line))
            insertKey(line[:-1], [], tr)
            targets.append(line[:-1])
    
    f.close()
    print("Loaded [%d] targets"%count)
    return targets
    
    
##################################################################################################################
# The process function...
##################################################################################################################
def process(trie, dnafile, targets):
    print("Processing file [%s], trie size [%d]"%(dnafile,len(trie)))
    i = 0
    j = 0
    tLen = 0
    remaining = 0
    marks = []
    
    with open(dnafile, 'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            j = i
            remaining = m.size()
            mSize = m.size()
            while i < mSize:
                remaining -= 1
                print(m[j:i+1])
                pList = startWithPrefix(m[j:i+1], trie, i)
                if pList == []:
                    j+=1
                else:
                    print(pList)
                    
                i+=1
            print("End; mmap size [%d], remaining [%d]"%(mSize,remaining))
            print()

##################################################################################################################
# The readTargets function accepts a file name as input and returns an array of targets contained within the file
##################################################################################################################   
def readTargets(file):
    #print("file %s"%file)
    targets = []
    
    with open(file) as f:
        for line in f:
            targets.append(line)
    
    #print(targets)
    f.close() 
    return targets

##################################################################################################################
# The indexDNABases function accepts a byte character and returns an integer representation for that input
##################################################################################################################
def indexDNABases(ch):
    #print(chr(ch))
    
    if chr(ch) == 'a' or chr(ch) == 'A':
        return 65 #'A'
    elif chr(ch) == 'c' or chr(ch) == 'C':
        return 67 #'C'
    elif chr(ch) == 'g' or chr(ch) == 'G':
        return 71 #'G'
    elif chr(ch) == 't' or chr(ch) == 'T':
        return 84 #'T'
    else:
        #print("Not a nucliotide base: "+chr(ch)) 
        return -1


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
        insertMarkers(k, v, trie)
        return None
    
def insertMarkers(k,v,trie):
    if k == '':
        return None
    #tr is now bound to the branch, insert a new bucket
    trie.append((k,[v]))
    return None
    

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
        
    newPrefix = norms.decode()
    
    br = retrieveBranch(newPrefix,trie)
    if br == None: return []
    
    keyList = []
    q = getChildBranches(br)
    
    while not q == []:
        currBr = q.pop()
        if isTrieBucket(currBr):
            keyList.append(getBucketKey(currBr))
            setBucketValue(currBr, v)
        elif isTrieBranch(currBr):
            q.extend(getChildBranches(currBr))
        else: return 'ERROR: bad branch'
    return keyList
    
    
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
# Test Functions
##################################################################################################################

def test_01():
    tr = [[]]
    insertKey("to", 7, tr)
    insertKey('tea', 3, tr)
    insertKey("ted", 4, tr)
    insertKey("A", 15, tr)
    insertKey("i", 11, tr)
    insertKey("in", 5, tr)
    insertKey("inn", 9, tr)
    return tr
    
def test_02():
    tr = test_01()
    
    print (startWithPrefix('t', tr))
    print (startWithPrefix('te', tr))
    print (startWithPrefix('i', tr))
    
    
##################################################################################################################
# Execute Main Function
##################################################################################################################
if __name__ == "__main__": main()