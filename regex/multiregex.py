'''
Created on 09.02.2016

@author: harald
'''
from automata.dfa import DFA
from automata.epsilon_nfa import EpsilonNFA
from automata.graphviz_automaton import draw
from regex.graphviz_regex import draw_parsetree
from regex.regex_parser import RegexParser


class MultiRegex(object):
    def __init__(self, iterable):
        # create list of NFAs
        self.parsetree = []
        self.nfa = EpsilonNFA(1, set(), 0, dict())
        for ind, reg in enumerate(iterable):
            parsetree = RegexParser.parse(reg)
            self.parsetree.append(parsetree)
            # draw_parsetree(parsetree, "parse%d.png" % ind)
            nfa = parsetree.eval().to_epsilon_nfa(ind)
            # NFA union
            self.nfa += nfa
            # remember automata
            
        
        # draw(self.nfa, "temp.png")
        # subset construction and minimization
        self.dfa = self.nfa.subset_construction().minimize()

    def match(self, strng):
        # transparently convert characters into ascii integers
        return self.dfa.match(ord(a) for a in strng)
    
    def draw(self, path):
        draw(self.dfa, path)
    
    
    
# class MultiRegexDFA(object):
#     def __init__(self, iterable):
#         # create list of NFAs
#         self.dfa = DFA(1, dict(), 0, dict())
#         for ind, reg in enumerate(iterable):
#             parsetree = RegexParser.parse(reg)
#             draw_parsetree(parsetree, "parse%d.png" % ind)
#             next_dfa = parsetree.eval().to_epsilon_nfa(ind).subset_construction().minimize()
#             self.dfa = self.dfa.union(next_dfa)
#             # self.dfa = self.dfa.minimize()
# 
#     def match(self, strng):
#         # transparently convert characters into ascii integers
#         return self.dfa.match(ord(a) for a in strng)
#     
#     def draw(self, path):
#         draw(self.dfa, path)
#         
#     def __eq__(self, other):
#         return self.dfa == other.dfa
#     
#     
# class MultiRegexNFA(object):
#     def __init__(self, iterable):
#         # create list of NFAs
#         self.nfa = EpsilonNFA(1, set(), 0, dict())
#         for ind, reg in enumerate(iterable):
#             parsetree = RegexParser.parse(reg)
#             draw_parsetree(parsetree, "parse%d.png" % ind)
#             nfa = parsetree.eval().to_epsilon_nfa(ind)
#             self.nfa += nfa
#         
# 
#     def match(self, strng):
#         # transparently convert characters into ascii integers
#         return self.nfa.match(ord(a) for a in strng)
#     
#     def draw(self, path):
#         draw(self.nfa, path)