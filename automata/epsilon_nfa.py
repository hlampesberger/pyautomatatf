import collections
import functools

from automata.dfa import DFA
from automata.helper import shift_transitions, mkunion


class EpsilonNFA(object):
    # final states are a map: Q -> Set(Label)
    def __init__(self, states, transitions, start, final):
        self.states = states
        self.transitions = transitions
        self.start = start
        self.final = final
        
        
    def __repr__(self):
        return "EpsilonNFA(%d, %s, %d, %s)" % (self.states, repr(self.transitions), self.start, repr(self.final))
    
    def __str__(self):
        return "EpsilonNFA(%d states, %d transitions)" % (self.states, len(self.transitions))


    def match(self, sequence):
        curr_states = frozenset({self.start})
        next_states = frozenset()        
        for a in sequence:
            next_states = self.next(curr_states, a)
            if not next_states:
                return set()
            curr_states = next_states
        
        fin = curr_states & self.final.keys()
        if fin:
            return {label for q in fin for label in self.final[q]}
        else:
            return set()


    @functools.lru_cache(maxsize=None)
    def epsilon_closure(self):
        # based on:
        # de la Higuera: Grammatical Inference (2010), p. 73, Algorithm 4.1
        closure = collections.defaultdict(set)
        for i in range(self.states):
            for j in range(self.states):
                if i == j:
                    closure[i].add(j)
                else:
                    if (i, 256, j) in self.transitions:
                        closure[i].add(j)
        for k in range(self.states):
            for i in range(self.states):
                for j in range(self.states):
                    if k in closure[i] and j in closure[k]:
                        closure[i].add(j)
        return closure

    def is_epsilon_free(self):
        return any(a == 256 for (_, a, _)  in self.transitions)


    @functools.lru_cache(maxsize=4096)
    def next_states(self, state, sym):
        closure = self.epsilon_closure()
        next_states = (qn for (q, _a, qn) in self.transitions if q in closure[state] and  _a == sym)
        return mkunion(closure[q] for q in next_states)

    @functools.lru_cache(maxsize=4096)
    def next(self, state_set, sym):
        return mkunion(self.next_states(q, sym) for q in state_set)


    @functools.lru_cache(maxsize=4096)
    def _succ(self, state):
        closure = self.epsilon_closure()
        succ = collections.defaultdict(set)
        for (q, a, qn) in self.transitions:
            if q in closure[state] and a is not 256:
                succ[a].update(closure[qn])
        return succ
    
    @functools.lru_cache(maxsize=4096)
    def successors(self, state_set):
        succ = collections.defaultdict(set)
        for q in state_set:
            for (a, states) in self._succ(q).items():
                succ[a].update(states)
        return succ
        

    def subset_construction(self):
        # based on:
        # Subset Construction presented by Ullman (Automata course)
        # extended with closure operation to work with epsilon transitions
        states = 1
        numeric_state = dict()
        closure = self.epsilon_closure()
        start = frozenset(closure[self.start])
        numeric_state[start] = states - 1
        finals = dict()

        # empty transitions dictionary
        tr = dict()
        
        queue = collections.deque([ start ])
        
        # if one of the subset states in the DFA start state is already final
        fin = start & self.final.keys()
        if fin:
            # start state is always id 0 
            finals[0] = {label for q in fin for label in self.final[q]}

        while queue:
            # print(len(queue))
            curr_state = queue.popleft()
            for (a, state_set) in self.successors(curr_state).items():         
            # for a in range(256):
                # next_state = self.next(curr_state, a)
                next_state = frozenset(state_set)

                if next_state:
                    # the state exists
                    if next_state not in numeric_state.keys():
                        states += 1
                        numeric_state[next_state] = states - 1
                        # add into queue so it gets resolved in next round
                        queue.append(next_state)

                    tr[numeric_state[curr_state], a] = numeric_state[next_state]
                    fin = next_state & self.final.keys()
                    if fin:
                        finals[numeric_state[next_state]] = {label for q in fin for label in self.final[q]}
        # print("State Subsets", numeric_state)
        return DFA(states, tr, 0, finals)


    def union(self, other):
        states = self.states + other.states
        start = self.start
        transitions = self.transitions | shift_transitions(other.transitions, self.states, self.states)
        transitions.add((start, 256, other.start + self.states))
        finals = self.final.copy()
        for k, v in other.final.items():
            finals[k + self.states] = v
        return EpsilonNFA(states, transitions, start, finals)
    # function alias
    __add__ = union

