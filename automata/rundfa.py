'''
Created on 12. Feb. 2016

@author: P24667
'''
from array import array
from automata.dfa import DFA
# import numpy as np

#### NOT USED, testing only! ####
class RunDFA(object):
    def __init__(self, dfa):
        assert(isinstance(dfa, DFA))
        self.dfa = dfa
        self.arr = array('i', (dfa.transitions.get((q, a), -1) for q in range(dfa.states) for a in range(256)))
        
        def getrow(q):
            return [dfa.transitions.get((q, a), -1) for a in range(256)]
        self.lst = [getrow(q) for q in range(dfa.states)]

    def match(self, seq):
        q = self.dfa.start
        for a in seq:
            q = self.lst[q][ord(a)]
            if q < 0: break
        return self.dfa.final.get(q, set())