'''
Created on 27.11.2014

@author: harald
'''
import random
import unittest

from automata.thompson_nfa import ThompsonNFA


class TestThompsonNFA(unittest.TestCase):


    def test_thompson_nfa_factory_methods(self):
        r = random.randint(0, 255)
        nfa = ThompsonNFA.character(r)
        self.assertIsInstance(nfa, ThompsonNFA, "Return value must be an instance of ThompsonNFA")
        self.assertEqual(nfa.states, 2, "The automaton must have exactly two states")
        self.assertEqual(len(nfa.transitions), 1, "The automaton must have exactly one transition")
        self.assertIn((nfa.start, r, nfa.final), nfa.transitions, "The single transition must be from start to end")

        lst = [22, 45, 112, 211]
        nfa = ThompsonNFA.character_class(lst)
        self.assertIsInstance(nfa, ThompsonNFA, "Return value must be an instance of ThompsonNFA")
        self.assertEqual(nfa.states, 2, "The automaton must have exactly two states")
        self.assertEqual(len(nfa.transitions), 4, "The automaton for the character clas test must have exactly 4 transitions")
        self.assertTrue(all((nfa.start, a, nfa.final) in nfa.transitions for a in lst), "At least one of the four transitions in the set has a bad character")
        
        nfa = ThompsonNFA.wildcard()
        self.assertIsInstance(nfa, ThompsonNFA, "Return value must be an instance of ThompsonNFA")
        self.assertEqual(nfa.states, 2, "The automaton must have exactly two states")
        self.assertEqual(len(nfa.transitions), 256, "The wildcard automaton must have exactly 256 transitions for symbols 0..255")
        self.assertTrue(all(q == nfa.start and 0 <= a <= 255 and qn == nfa.final for (q, a, qn) in nfa.transitions), "At least one of the transitions in the set has a bad character")


    
    def test_thompson_nfa_choice1(self):
        # little sequence test to be sure
        nfa = ThompsonNFA.empty().concat(ThompsonNFA.empty())
        self.assertEqual(nfa.states, 3, "The automaton must have 3 states")
        nfa1 = ThompsonNFA(2, {(0, 15, 1)}, 0, 1)
        nfa2 = ThompsonNFA(2, {(0, 32, 1)}, 0, 1)
        nfa = nfa1.choice(nfa2)
        self.assertIsInstance(nfa, ThompsonNFA, "The returned automaton must be an instance of ThompsonNFA")
        self.assertEqual(nfa.states, 6, "The returned choice() automaton must have 6 states = 2 nfa1 + 2 nfa2 + 1 new start + 1 new final")

    def test_thompson_nfa_choice2(self):
        nfa1 = ThompsonNFA(2, {(0, 15, 1)}, 0, 1)
        nfa2 = ThompsonNFA(2, {(0, 32, 1)}, 0, 1)
        nfa = nfa1.choice(nfa2)
        next_states = {qn for (q, a, qn) in nfa.transitions if q == nfa.start and a == 256}
        self.assertEqual(len(next_states), 2, "For choice() there must be two epsilon transitions from the new start to the old start1 and old start2")
        tr = {(q, a, qn) for (q, a, qn) in nfa.transitions if q in next_states}
        self.assertEqual(len(tr), 2, "For choice() the original transitions were somehow tampered")
        self.assertFalse(any(a for (q, a, qn) in tr if a == 256), "For choice() the original transitions were somehow tampered, there is an epsilon transition where it shouldn't be")
        old_ends = {qn for (q, a, qn) in tr}
        next_states = {qn for (q, a, qn) in nfa.transitions if q in old_ends and a == 256}
        self.assertEqual(len(next_states), 1, "For choice() there must be two epsilon transitions from the old final1 and old final2 to the new final")
        self.assertEqual(next_states.pop(), nfa.final, "For choice() the two epsilon transitions from the old final1 and old final2 do not point to the new final")

    
    def test_thompson_nfa_iteration1(self):
        nfa = ThompsonNFA(2, {(0, 15, 1)}, 0, 1).iteration()
        self.assertIsInstance(nfa, ThompsonNFA, "The returned automaton must be an instance of ThompsonNFA")
        self.assertEqual(nfa.states, 4, "The returned iteration() automaton must have 4 states = 2 before + 1 new start + 1 new final")

    def test_thompson_nfa_iteration2(self):
        nfa = ThompsonNFA(2, {(0, 15, 1)}, 0, 1).iteration()
        self.assertIn((nfa.start, 256, nfa.final), nfa.transitions, "For iteration() there needs to be an epsilon transition from start to final state")
        next_state = {qn for (q, a, qn) in nfa.transitions if q == nfa.start and a == 256 and qn != nfa.final}
        self.assertEqual(len(next_state), 1, "For iteration() there must be exactly one epsilon transition from the new start to the old start")
        old_start = next_state.pop()
        next_state = {qn for (q, a, qn) in nfa.transitions if q == old_start and a == 15}
        self.assertEqual(len(next_state), 1, "For iteration() the original transitions were somehow tampered")
        old_end = next_state.pop()
        next_state = {qn for (q, a, qn) in nfa.transitions if q == old_end and a == 256 and qn == nfa.final}
        self.assertEqual(len(next_state), 1, "For iteration() there must be exactly one epsilon transition from the old final to the new final")
        next_state = {qn for (q, a, qn) in nfa.transitions if q == old_end and a == 256 and qn == old_start}
        self.assertEqual(len(next_state), 1, "For iteration() there must be exactly one epsilon transition from the old final to the old start")        

#     def test_thompson_nfa_export(self):
#         nfa = ThompsonNFA.empty() * ThompsonNFA.empty()
#         enfa = nfa.to_epsilon_nfa(22)
#         self.assertIsInstance(enfa, EpsilonNFA, "The returned automaton must be of type EpsilonNFA")
#         self.assertEqual(enfa.states, 3, "The exported EpsilonNFA must have 3 states")
#         self.assertEqual(set(enfa.final_states.keys()), {nfa.final}, "The final states in the EpsilonNFA must be the single final state from the nfa")
#         self.assertEqual(enfa.final_states[nfa.final], {22}, "The label was not handed correctly to the EpsilonNFA")
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()