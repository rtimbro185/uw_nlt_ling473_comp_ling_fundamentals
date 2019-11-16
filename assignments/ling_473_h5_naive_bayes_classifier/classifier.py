#!/opt/python-3.4/bin/python3.4
#  -*- coding: utf-8 -*-

#Author: Ryan Timbrook
#Date: 
#Project:
      
from collections import defaultdict
from math import log10, floor

class LMFrequencyDist(object):
    
    def __init__(self,lang):
        self.langId = lang
        self.wordCounts = []
        self.wordMap = {}
        self.countMap = {}
        self.invertedCountMap = {}
        self.__le__ = len(self.wordCounts)
    
    def _le_(self):
        return len(self.wordCounts)
  
    def getLangId(self):
        return self.langId
    
    def setWordCounts(self,wc):
        self.wordCounts.append(wc)
        
    def utilCreateWordMaps(self):
        self.wordMap = dict((w[0],i) for (i,w) in enumerate(self.wordCounts))
        self.countMap = dict((i,c[1]) for (i,c) in enumerate(self.wordCounts))
       
    def N(self):
        return sum(self.countMap.values())
    
    def keys(self):
        return self.wordMap.keys()
    
    def values(self):
        return self.countMap.values()
    
    def keyIndex(self,key):
        return self.wordMap[key]
       
    def wordCount(self,idx):
        v = self.countMap[idx]
        return v
    
    def freq(self,word):
        if self.N() == 0:
            return 0
        if word in self.keys():
            return self.wordCount(self.wordMap[word]) / self.N()
        else:
            return 1
    
    def __str__(self):
        return 'LMFrequencyDist with %d samples and %d outcomes' % (self._le_(), self.N())

    
class TextProbDist(object):
    
    def __init__(self,identifier, sentence, textFrags):
        self.identifier = identifier
        self.sentence = sentence
        self.text_fragments = textFrags
        self._key = identifier,sentence
        self.wordProbabilities = {}
        self.languageProbabilities = {}
        self.languageIdentifier = None
        
    def __eq__(self, other):
        return self._key == other._key
    
    def __hash__(self):
        return hash(self._key)   
        
    def setWordProbabilities(self,text,p):
        self.wordProbabilities[text] = p
        
    def setLanguageProbabilities(self,lang,p):
        self.languageProbabilities[lang] = p
    
    def prob(self,wc,ts):
        p = log10(wc/ts)
        return p
    
    def logprob(self):
        v = self.wordProbabilities.values()
        v = list(v)
        p = float(0)
        p = v[:1]
        p = self.roundLogFloorSig(p[0])
        for e in v[1:]:
            p = self.roundLogFloorSig(p+e)   
        return p
    
    def smooth(self,sampleSize):
        s = self.prob(1.0, float(sampleSize))
        return s
        
    def textFragments(self):
        return self.text_fragments
       
    def max(self):
        probs = []
        for v in self.languageProbabilities.values():
            probs.append(v)
        argmax = probs[probs.index((max(probs)))]
        argmaxLang = dict(map(reversed,self.languageProbabilities.items()))[argmax]
        self.languageIdentifier = argmaxLang
        
    def roundLogFloorSig(self,x,sig=10):
        return round(x,sig-int(floor(log10(abs(x))))-1)
    
    def printOutput(self):
        print("{0}\t{1}".format(self.identifier,self.sentence))
        for k,v in self.languageProbabilities.items():
            print("{0}\t{1}".format(k,v))
        print("{0}\t{1}".format("result",self.languageIdentifier))
        
        
        
    
    