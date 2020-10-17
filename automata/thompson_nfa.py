'''
Created on 25.09.2014

@author: harald
'''
from automata.helper import shift_transitions
from automata.epsilon_nfa import EpsilonNFA

class ThompsonNFA(object):
    """ Thompson NFA is a special NFA with epsilon transitions and a single final state
        for alphabet over bytes = symbols 0..255
        plus an extra symbol for epsilon transition (256)
        states are integers """
    def __init__(self, states, transitions, start, final):
        assert(isinstance(states, int))
        assert(isinstance(transitions, set))
        self.states = states
        self.transitions = transitions
        self.start = start
        self.final = final

        
    def __repr__(self):
        return "ThompsonNFA(%d, %s, %d, %d)" % (self.states, repr(self.transitions), self.start, self.final)

    def __str__(self):
        return "ThompsonNFA(%d states, %d transitions)" % (self.states, len(self.transitions))

    def concat(self, other):
        # final of self will become start of other
        # therefore one state less in other
        states = self.states + other.states - 1
        transitions = self.transitions.copy()
        def fun(q):
            if q == other.start: return self.final
            else: return q + self.states - 1
        transitions.update((fun(q), a, fun(qn)) for (q, a, qn) in other.transitions)
        return ThompsonNFA(states, transitions, self.start, fun(other.final))

    def choice(self, other):
        # new start and new final state
        # epsilon transitions in between
        states = self.states + other.states + 2
        start = 0
        final = 1
        transitions = shift_transitions(self.transitions, 2, 2)
        transitions.update(shift_transitions(other.transitions, self.states + 2, self.states + 2))
        transitions.add((start, 256, self.start + 2))
        transitions.add((start, 256, other.start + self.states + 2))
        transitions.add((self.final + 2, 256, final))
        transitions.add((other.final + self.states + 2, 256, final))
        return ThompsonNFA(states, transitions, start, final)

    def iteration(self):
        states = self.states + 2
        start = 0
        final = 1
        transitions = shift_transitions(self.transitions, 2, 2)
        transitions.add((start, 256, final))
        transitions.add((start, 256, self.start + 2))
        transitions.add((self.final + 2, 256, final))
        transitions.add((self.final + 2, 256, self.start + 2))
        return ThompsonNFA(states, transitions, start, final)

    def plus(self):
        states = self.states + 2
        start = 0
        final = 1
        transitions = shift_transitions(self.transitions, 2, 2)
        # transitions.add((start, 256, final))
        transitions.add((start, 256, self.start + 2))
        transitions.add((self.final + 2, 256, final))
        transitions.add((self.final + 2, 256, self.start + 2))
        return ThompsonNFA(states, transitions, start, final)

    def plus2(self):
        transitions = self.transitions.copy()
        transitions.add((self.final, 256, self.start))
        return ThompsonNFA(self.states, transitions, self.start, self.final)

    def eventually(self):
        transitions = self.transitions.copy()
        transitions.add((self.start, 256, self.final))
        return ThompsonNFA(self.states, transitions, self.start, self.final)

    @staticmethod
    def empty():
        return ThompsonNFA(2, {(0, 256, 1)}, 0, 1)

    @staticmethod
    def character(c):
        assert(0 <= c <= 255)
        return ThompsonNFA(2, {(0, c, 1)}, 0, 1)

    @staticmethod
    def character_class(character_set):
        transitions = {(0, c, 1) for c in character_set}
        return ThompsonNFA(2, transitions, 0, 1)

    @staticmethod
    def wildcard():
        transitions = {(0, c, 1) for c in range(256)}
        return ThompsonNFA(2, transitions, 0, 1)

    @staticmethod
    def dotstar():
        transitions = {(0, c, 0) for c in range(256)}
        return ThompsonNFA(1, transitions, 0, 0)

    @staticmethod
    def dotplus():
        transitions = {(0, c, 1) for c in range(256)}
        transitions.add((1, 256, 0))
        return ThompsonNFA(2, transitions, 0, 1)

    def to_epsilon_nfa(self, ftype):
        f = {self.final: {ftype}}
        return EpsilonNFA(self.states, self.transitions, self.start, f)


