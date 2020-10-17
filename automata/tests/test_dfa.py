'''
Created on 27.11.2014

@author: harald
'''
import unittest

from automata.dfa import DFA


class TestDFA(unittest.TestCase):


    def test_dfa_match_empty(self):
        tr = {(0, 15): 1,
              (0, 22): 2,
              (1, 17): 3,
              (2, 17): 3,
              (2, 22): 4,
              (3, 22): 4,
              (4, 233): 4
              }
        fs = {1: {'regex1'},
              4: {'regex2'}
              }
        dfa = DFA(5, tr, 0, fs)
        seq = []
        self.assertEqual(dfa.match(seq), set(), "Matching the empty sequence should stay in the start state which is not final")
        tr = {(0, 15): 0}
        fs = {0: {'regex1'}}
        dfa = DFA(1, tr, 0, fs)
        self.assertEqual(dfa.match([]), {"regex1"}, "In this example, the start state is accepting, so the empty sequence should return the correct label")


    def test_dfa_match_bad(self):
        tr = {(0, 15): 1,
              (0, 22): 2,
              (1, 17): 3,
              (2, 17): 3,
              (2, 22): 4,
              (3, 22): 4,
              (4, 233): 4
              }
        fs = {1: {'regex1'},
              4: {'regex2'}
              }
        dfa = DFA(5, tr, 0, fs)
        seq = [2]
        self.assertEqual(dfa.match(seq), set(), "Matching the empty sequence should stay in the start state which is not final in this example")
        
        tr = {(0, 15): 1,
              (0, 22): 2,
              (1, 17): 3,
              (2, 17): 3,
              (2, 22): 4,
              (3, 22): 4,
              (4, 233): 4
              }
        fs = {1: {'regex1'},
              4: {'regex2'}
              }
        dfa = DFA(5, tr, 0, fs)
        seq = [22, 22, 233, 2]
        self.assertEqual(dfa.match(seq), set(), "If a transition is undefined, it must return set()")


    def test_dfa_match_good1(self):
        tr = {(0, 15): 1,
              (0, 22): 2,
              (1, 17): 3,
              (2, 17): 3,
              (2, 22): 4,
              (3, 22): 4,
              (4, 233): 4
              }
        fs = {1: {'regex1'},
              4: {'regex2'}
              }
        dfa = DFA(5, tr, 0, fs)
        seq = [15]
        self.assertEqual(dfa.match(seq), {'regex1'}, "In this example, the sequence [15] leads into final state 1 that should return regex1 as label")

        tr = {(0, 15): 1,
              (0, 22): 2,
              (1, 17): 3,
              (2, 17): 3,
              (2, 22): 4,
              (3, 22): 4,
              (4, 233): 4
              }
        fs = {1: {'regex1'},
              4: {'regex2'}
              }
        dfa = DFA(5, tr, 0, fs)
        seq = [15, 17, 22, 233]
        self.assertEqual(dfa.match(seq), {'regex2'}, "In this example, the sequence [15, 17, 22, 233] leads into final state 4 that should return regex2 as label")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()