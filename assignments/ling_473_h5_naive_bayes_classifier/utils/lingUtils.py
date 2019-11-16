'''
Created on Sep 5, 2016

@author: RTimbro1
'''
import pprint
from collections import defaultdict

class FreqDistDocument(object):
    
    def __init__(self,identifier,sentence):
        self.identifier = identifier
        self.sentence = sentence
        self._key = identifier,sentence
        self.languageModelRankings = []
        self.wordProbabilities = defaultdict(list)
        self.languageIdentifier = None
    
    def __eq__(self, other):
        return self._key == other._key
    
    def __hash__(self):
        return hash(self._key)
    
    def addLanguageModelRankings(self,rankings):
        self.languageModelRankings.append(rankings)
    
    def setLanguageIdentifier(self,langIdt):
        self.languageIdentifier = langIdt
    
    def addWordProbabilities(self,lang,p):
        self.wordProbabilities[lang].append(p)
        
        
    def printResults(self):
        pprint.pprint("{0}\t{1}".format(self.identifier,self.sentence))
        for lang in self.languageModelRankings():
            pprint.pprint("{0}\t{1}".format((k,v) for k, v in lang.items()))
        pprint.pprint("result\t{0}".format(self.languageIdentifier))