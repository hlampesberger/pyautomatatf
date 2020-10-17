'''
Created on 27.11.2014

@author: harald
'''
import unittest

from automata.thompson_nfa import ThompsonNFA
from regex.regex import Character, Alphanum, AnyCharacter, Expression, \
    Iteration, Sequence, Choice


class TestRegex(unittest.TestCase):


    def test_regex_eval_character_anycharacter(self):
        r = Character(Alphanum('a'))
        nfa = r.eval()
        self.assertIsInstance(nfa, ThompsonNFA, "eval() must return a ThompsonNFA")
        self.assertEqual(nfa.states, 2, "For a single ASCII symbol, the automaton should have size 2")
        self.assertIn((nfa.start, ord('a'), nfa.final), nfa.transitions, "The transition in the ThompsonNFA is bad")
        r = AnyCharacter('.')
        nfa = r.eval()
        self.assertIsInstance(nfa, ThompsonNFA, "eval() must return a ThompsonNFA")
        self.assertEqual(nfa.states, 2, "For a single ASCII symbol, the automaton should have size 2")
        self.assertEqual(len(nfa.transitions), 256, "The wildcard automaton must have 256 transitions for every character")
    
    def test_regex_eval_expression_iteration(self):
        r = Expression(Character(Alphanum('a')))
        s = Character(Alphanum('a'))
        nfa1 = r.eval()
        nfa2 = s.eval()
        self.assertIsInstance(nfa1, ThompsonNFA, "eval() must return a ThompsonNFA")
        self.assertEqual(nfa1.states, 2, "For a single ASCII symbol, the automaton should have size 2")
        self.assertEqual(nfa1.transitions, nfa2.transitions, "Expression should not modify the ThompsonNFA created by its child")
        r = Iteration(Character(Alphanum('a')))
        nfa = r.eval()
        self.assertIsInstance(nfa, ThompsonNFA, "eval() must return a ThompsonNFA")
        self.assertEqual(nfa.states, 4, "For a single ASCII symbol and Iteration, the automaton should have size 4")
        self.assertIn((nfa.start, 256, nfa.final), nfa.transitions, "For iteration() there needs to be an epsilon transition from start to final state")
        next_state = {qn for (q, a, qn) in nfa.transitions if q == nfa.start and a == 256 and qn != nfa.final}
        self.assertEqual(len(next_state), 1, "For iteration() there must be exactly one epsilon transition from the new start to the old start")
        old_start = next_state.pop()
        next_state = {qn for (q, a, qn) in nfa.transitions if q == old_start and a == ord('a')}
        self.assertEqual(len(next_state), 1, "For iteration() the original transitions were somehow tampered")
        old_end = next_state.pop()
        next_state = {qn for (q, a, qn) in nfa.transitions if q == old_end and a == 256 and qn == nfa.final}
        self.assertEqual(len(next_state), 1, "For iteration() there must be exactly one epsilon transition from the old final to the new final")
        next_state = {qn for (q, a, qn) in nfa.transitions if q == old_end and a == 256 and qn == old_start}
        self.assertEqual(len(next_state), 1, "For iteration() there must be exactly one epsilon transition from the old final to the old start")        


    def test_regex_eval_sequence_choice(self):
        r = Sequence(Character(Alphanum('a')), Character(Alphanum('b')))
        nfa = r.eval()
        self.assertIsInstance(nfa, ThompsonNFA, "eval() must return a ThompsonNFA")
        self.assertEqual(nfa.states, 3, "For Sequence of 'a' and 'b' the automaton must have 3 states")
        next_state = {qn for (q, a, qn) in nfa.transitions if q == nfa.start and a == ord('a')}
        self.assertEqual(len(next_state), 1, "For sequence(), the original transitions were somehow tampered")
        tmp = next_state.pop()
        self.assertNotEqual(tmp, nfa.final, "For squence(), the middle state must not be accepting")
        next_state = {qn for (q, a, qn) in nfa.transitions if q == tmp and a == ord('b')}
        self.assertEqual(len(next_state), 1, "For sequence(), the original transitions were somehow tampered")
        self.assertEqual(next_state.pop(), nfa.final, "For sequence(), the state after 'ab' in this example must be nfa.final")
        
        r = Choice(Character(Alphanum('a')), Character(Alphanum('b')))
        nfa = r.eval()
        self.assertIsInstance(nfa, ThompsonNFA, "eval() must return a ThompsonNFA")
        self.assertEqual(nfa.states, 6, "For Choice of 'a' and 'b' the automaton must have 6 states")
        next_states = {qn for (q, a, qn) in nfa.transitions if q == nfa.start and a == 256}
        self.assertEqual(len(next_states), 2, "For choice() there must be two epsilon transitions from the new start to the old start1 and old start2")
        tr = {(q, a, qn) for (q, a, qn) in nfa.transitions if q in next_states}
        self.assertEqual(len(tr), 2, "For choice() the original transitions were somehow tampered")
        self.assertFalse(any(a for (q, a, qn) in tr if a == 256), "For choice() the original transitions were somehow tampered, there is an epsilon transition where it shouldn't be")
        old_ends = {qn for (q, a, qn) in tr}
        next_states = {qn for (q, a, qn) in nfa.transitions if q in old_ends and a == 256}
        self.assertEqual(len(next_states), 1, "For choice() there must be two epsilon transitions from the old final1 and old final2 to the new final")
        self.assertEqual(next_states.pop(), nfa.final, "For choice() the two epsilon transitions from the old final1 and old final2 do not point to the new final")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()