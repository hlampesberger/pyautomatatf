'''
Created on 27.11.2014

@author: harald
'''
import unittest
from automata.epsilon_nfa import EpsilonNFA

class TestEpsilonNFA(unittest.TestCase):
    def test_epsilon_nfa_combine1(self):
        nfa1 = EpsilonNFA(2, {(0, 22, 1)}, 0, {1: 'nfa1'})
        nfa2 = EpsilonNFA(2, {(0, 15, 1)}, 0, {1: 'nfa2'})
        nfa = nfa1.union(nfa2)
        self.assertIsInstance(nfa, EpsilonNFA, "The returned automaton must be of type EpsilonNFA")
        self.assertEqual(nfa.states, 4, "The number of states in the returned EpsilonNFA must be the sum of states of the combined automata")

    def test_epsilon_nfa_combine2(self):
        nfa1 = EpsilonNFA(2, {(0, 22, 1)}, 0, {1: 'nfa1'})
        nfa2 = EpsilonNFA(2, {(0, 15, 1)}, 0, {1: 'nfa2'})
        nfa = nfa1.union(nfa2)
        next_state = {qn for (q, a, qn) in nfa.transitions if q == nfa.start and a == 22}
        self.assertEqual(len(next_state), 1, "In combine(), the transitions of self were modified but they shouldn't")
        self.assertEqual(nfa.final[next_state.pop()], 'nfa1', "In combine(), the label of ex-self's final states seems to be wrong")
        next_state = {qn for (q, a, qn) in nfa.transitions if q == nfa.start and a == 256}
        self.assertEqual(len(next_state), 1, "In this combine() test, there must be a single epsilon transition from nfa.start to other's former start state")
        other_start = next_state.pop()
        next_state = {qn for (q, a, qn) in nfa.transitions if q == other_start and a == 15}
        self.assertEqual(len(next_state), 1, "In combine(), the transitions of other seem to be broken")
        self.assertEqual(nfa.final[next_state.pop()], 'nfa2', "In combine(), the label of ex-other's final states seems to be wrong")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()