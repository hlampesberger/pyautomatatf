import collections
import functools


class DFA(object):
    # alphabet 0..255
    # NO epsilon transitions!
    def __init__(self, states, transitions, start, fin):
        self.states = states
        self.transitions = transitions
        self.start = start
        self.final = fin
        
    def __repr__(self):
        return "DFA(%d, %s, %d, %s)" % (self.states, repr(self.transitions), self.start, repr(self.final))
    
    def __str__(self):
        return "DFA(%d states, %d transitions)" % (self.states, len(self.transitions))

    def match(self, sequence):
        try:
            q = self.start
            for a in sequence:
                q = self.transitions[q, a]
            return self.final.get(q, set())
        except KeyError:
            return set()

    # @functools.lru_cache(maxsize=None)
    def _successors(self, state):
        return {qn for (k, qn) in self.transitions.items() if k[0] == state and qn != state}


    def is_empty(self):
        # depth first search from start to check whether an accepting state
        # is reachable or not
        frontier = [self.start]
        visited = set()
        while frontier:
            # print(frontier)
            q = frontier.pop()
            if q not in visited:
                visited.add(q)
                if self.final.get(q, set()):
                    # early exit
                    return False 
                for qn in self._successors(q):
                    if qn not in visited:
                        frontier.append(qn)
        return True


    def _myhill_nerode_equiv_classes(self):
        # partition refinement by Hopcroft (1971) from Wikipedia
        # http://en.wikipedia.org/wiki/DFA_minimization
        not_accepting_states = {q for q in range(self.states) if q not in self.final}
        not_accepting_states = frozenset(not_accepting_states)

        # group final_states by their types, so different final states are not in the same equivalence class
        v = collections.defaultdict(set)
        for key, value in sorted(self.final.items()):
            v[frozenset(value)].add(key)
        accepting_states = list(frozenset(eq_final) for eq_final in v.values())

        P = accepting_states + [not_accepting_states]
        W = accepting_states

        # working off the work queue
        while W:
            S = W.pop()
            pred_groups = collections.defaultdict(set)
            for key, value in self.transitions.items():
                if value in S:
                    pred_groups[key[1]].add(key[0])
            
            for inv_states in pred_groups.values():
            # for a in range(256):
                # inv_states = {s for s in range(-1, self.states) if self.transitions.get((s, a), -1) in S}
                Pnew = []
                for R in P:
                    R1 = R & inv_states
                    if R1 and not (R.issubset(inv_states)):
                        R2 = R - R1
                        Pnew.append(R1)
                        Pnew.append(R2)
                        if R in W:
                            W.remove(R)
                            W.append(R1)
                            W.append(R2)
                        else:
                            W.append(min(R1, R2, key=len))
                    else:
                        Pnew.append(R)
                P = Pnew
        return P


    def minimize(self):
        # we assume state -1 as a dead state for incomplete transitions
        # we do not need to delete unreachable states -> they are reachable by construction from a RE
        # self.del_unreachable_states()
        eq_classes = self._myhill_nerode_equiv_classes()
        
        # construct new DFA with minimal states
        transitions = dict()
        start = None
        finals = dict()
        
        # set_ref : States --> EquivClasses
        set_ref = dict()
        for c in eq_classes:
            for state in c:
                set_ref[state] = c
        enum = {c: i for i, c in enumerate(eq_classes) if c}
        states = len(enum)
        
        for c in eq_classes:
            # ignore trap state
            # if -1 not in c:
            if c:
                # not empty
                # if all states are accepting, there could be an empty c
                if self.start in c:
                    if start is not None:
                        raise RuntimeError("Start state in multiple classes!")
                    else:
                        start = enum[c]
                fin = c & self.final.keys() 
                if fin:
                    for q in fin:
                        # pick final state labels from the first in fin
                        # all others in the equivalence class are guaranteed to have the same label
                        finals[enum[c]] = self.final[q]
                        break
    
                # choose transitions from one representative in the equivalence class
                for q in c:
                    for key, qn in self.transitions.items():
                        if key[0] == q:
                            transitions[enum[c], key[1]] = enum[set_ref[qn]]       
                    break
        return DFA(states, transitions, start, finals)




    def product(self, other, fop):
        assert(isinstance(other, DFA))
        states = 1
        numeric_state = dict()
        start = (self.start, other.start)
        numeric_state[start] = 0
        final = dict()
        tr = dict()
        
        queue = collections.deque([start])

        ftypes = fop(self.final.get(self.start, set()), other.final.get(other.start, set()))
        if ftypes:
            final[0] = ftypes

        while queue:
            curr_state = queue.popleft()
            for a in range(256):
                left_next = self.transitions.get((curr_state[0], a), -1)
                right_next = other.transitions.get((curr_state[1], a), -1)
                
                if left_next >= 0 or right_next >= 0:
                    next_state = (left_next, right_next)
                    if next_state not in numeric_state.keys():
                        numeric_state[next_state] = states
                        states += 1
                        queue.append(next_state)
                    tr[numeric_state[curr_state], a] = numeric_state[next_state]
                    
                    ftypes = fop(self.final.get(left_next, set()), other.final.get(right_next, set()))
                    if ftypes:
                        final[numeric_state[next_state]] = ftypes
   
        return DFA(states, tr, 0, final)     
    
    def union(self, other):    
        def fop(s1, s2): return s1.union(s2)
        return self.product(other, fop) 
    __or__ = union
   
    def intersection(self, other):
        def fop(s1, s2): return s1.intersection(s2)
        return self.product(other, fop)
    __and__ = intersection
   
    def difference(self, other):
        def fop(s1, s2): return s1.difference(s2)
        return self.product(other, fop)
    __sub__ = difference
   
    def xor(self, other):
        def fop(s1, s2): return s1.symmetric_difference(s2)
        return self.product(other, fop)
    __xor__ = xor

    def is_subset(self, other):
        pass

    def is_equivalent(self, other):
        return self.xor(other).is_empty()
    __eq__ = is_equivalent

