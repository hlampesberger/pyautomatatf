'''
Created on 09.02.2016

@author: harald
'''

from regex.multiregex import MultiRegex
from automata.graphviz_automaton import draw
from regex.graphviz_regex import draw_parsetree

if __name__ == '__main__':
    reg = MultiRegex([r"^aaab", r"^abc?"])
    print(reg.nfa)
    print(reg.dfa) # minimized
    
    draw(reg.dfa, "example.png")

    