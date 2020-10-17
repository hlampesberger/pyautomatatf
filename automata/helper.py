'''
Created on 26.11.2014

@author: hlampesberger
'''

# for tuples (q, a, qn) in transition set, create a new set with tuples,
# where q is incremented by inc_q and qn is incremented by inc_qn
def shift_transitions(transition_set, inc_q, inc_qn):
    return {(q + inc_q, a, qn + inc_qn) for (q, a, qn) in transition_set}

# union of a list of sets
def mkunion(arg):
    return frozenset(elem for S in arg for elem in S)
