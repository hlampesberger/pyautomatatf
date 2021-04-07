from automata.graphviz_automaton import draw
from regex.regex_parser import RegexParser


if __name__ == '__main__':
    print("==== CASE 1 ====")
    r1 = "^ABCD"
    r2 = "ABCD"
    #nfa1 = RegexParser.parse(r1).eval().to_epsilon_nfa(1)
    ##print(nfa1.subset_construction())
    nfa2 = RegexParser.parse(r2).eval().to_epsilon_nfa(2)
    print(nfa2)
    dfa = nfa2.subset_construction()
    print(dfa)
    draw(dfa, "case1.png")

    
    print("==== CASE 2 ====")
    r1 = "^AB.*CD"
    nfa1 = RegexParser.parse(r1).eval().to_epsilon_nfa(1)
    print(nfa1)
    dfa = nfa1.subset_construction()
    print(dfa)
    draw(dfa, "case2.png")
    

    print("==== CASE 3 ====")
    r1 = "^AB?B?B?B?B?CD"
    nfa1 = RegexParser.parse(r1).eval().to_epsilon_nfa(1)
    print(nfa1)
    dfa = nfa1.subset_construction()
    print(dfa)
    draw(dfa, "case3.png")

    
    print("==== CASE 4 ====")
    r1 = "^AA*[ABCDEFGHIJKLMNOPQRSTUVWXYZ]?[ABCDEFGHIJKLMNOPQRSTUVWXYZ]?[ABCDEFGHIJKLMNOPQRSTUVWXYZ]?[ABCDEFGHIJKLMNOPQRSTUVWXYZ]?[ABCDEFGHIJKLMNOPQRSTUVWXYZ]?[ABCDEFGHIJKLMNOPQRSTUVWXYZ]?CD"
    nfa1 = RegexParser.parse(r1).eval().to_epsilon_nfa(1)
    print(nfa1)
    dfa = nfa1.subset_construction()
    print(dfa)
    draw(dfa, "case4.png")



    print("==== CASE 5 ====")
    r1 = "AB......*CD"
    nfa1 = RegexParser.parse(r1).eval().to_epsilon_nfa(1)
    draw(nfa1, "nfa_case5.png")
    print(nfa1)
    dfa = nfa1.subset_construction()
    print(dfa)
    draw(dfa, "case5.png")
