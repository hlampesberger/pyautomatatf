'''
Created on 09.02.2016

@author: harald
'''

from regex.multiregex import MultiRegex
from automata.graphviz_automaton import draw
from regex.graphviz_regex import draw_parsetree

if __name__ == '__main__':
    reg1 = MultiRegex([r"^GET HTTP", r"^GET (HTTP|FTP) Version( 1\.1)?", r"#yolo"])
    print(reg1.nfa)
    print(reg1.dfa) # minimized
    
    for ind, pt in enumerate(reg1.parsetree):
        draw_parsetree(pt, "parse{0}.png".format(ind))
     
    draw(reg1.dfa, "dfa.png")
    draw(reg1.nfa, "nfa.png")

    print(reg1.match("GET HTTP #yolo"))
     
    
    
    reg2 = MultiRegex([r"[Ww][Ii][Nn]32\.[Ee][Xx][Ee]"])
    dfa = reg2.nfa.subset_construction()
    draw(reg2.nfa, "before.png")
    draw(dfa, "unminimized.png")
    draw(reg2.dfa, "minimized.png")

    