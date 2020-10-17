'''
Created on 26.09.2014

@author: hlampesberger
'''
import collections
import itertools
import os
import string
import subprocess
import tempfile

from automata.dfa import DFA
from automata.epsilon_nfa import EpsilonNFA
from automata.thompson_nfa import ThompsonNFA


def draw(obj, path):
    (fd, filename) = tempfile.mkstemp()
    try:
        tfile = os.fdopen(fd, "w")
        export_graphviz(obj, tfile)
        tfile.close()
        dot = which("dot")
        if dot is None:
            if os.name == "nt":
                dot = "dot"
            else:
                # OSX workaround
                dot = "/opt/local/bin/dot"
        if path.endswith(".png"):
            subprocess.call([dot, "-Tpng" , "-o", path, filename], shell=True)
        elif path.endswith(".pdf"):
            subprocess.call([dot, "-Tpdf" , "-o", path, filename], shell=True)
        else:
            raise RuntimeError("Unknown graphiz export file format.")
    finally:
        os.remove(filename)


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
 
    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
 
    return None


# magic that turns a list list of integers into strings of ranges
def format_chr(i):
    asc = chr(i)
    if asc == ' ':
        return "Space"
    elif asc == '\t':
        return '\\\\t'
    elif asc == '\r':
        return '\\\\r'
    elif asc == '\f':
        return '\\\\f'
    elif asc == '\n':
        return '\\\\n'
    elif asc == '\\':
        return '\\\\'
    elif asc in string.ascii_letters or asc in "01234567890?%&$+-_/.":
        return asc
    else:
        return str(hex(i))

def format_ranges(i):
    def key(tpl):
        return tpl[1] - tpl[0]
    for (_, b) in itertools.groupby(enumerate(sorted(i)), key):
        b = list(b)
        left = b[0][1]
        right = b[-1][1]
        if left == 0 and right == 255:
            yield "Any"
        elif left == right:
            if left == 256:
                yield "&#949;"
            else:
                yield format_chr(left)
        else:
            if right == 256:
                if left == 0:
                    yield "Any"
                else:
                    yield "%s-%s" % (format_chr(left), format_chr(right - 1))
                yield "&#949;"
            else:
                yield "%s-%s" % (format_chr(left), format_chr(right))




def export_graphviz(obj, fd):
    if isinstance(obj, DFA): export_graphviz_dfa(obj, fd)
    elif isinstance(obj, EpsilonNFA): export_graphviz_epsilon_nfa(obj, fd)
    elif isinstance(obj, ThompsonNFA): export_graphviz_thompson_nfa(obj, fd)
    else: raise RuntimeError("graphviz export not defined", obj)

def export_graphviz_dfa(automaton, fd):
    # header
    fd.write("digraph G {\n")
    fd.write("  rankdir=LR;\n")
    # content
    for s in range(automaton.states):
        if s in automaton.final.keys():
            fd.write("  n%d [label=\"%d\",xlabel=\"%s\",shape=\"doublecircle\"];\n" % (s, s, automaton.final[s]))
            # fd.write("  n%d [label=\"%d\",shape=\"doublecircle\"];\n" % (s, s))
        else:
            fd.write("  n%d [label=\"%s\",shape=\"circle\"];\n" % (s, s))

    # dummy start
    fd.write("  START%d [shape=\"point\",color=\"white\",fontcolor=\"white\"];\n" % automaton.start)
    fd.write("  START%d -> n%d;\n" % (automaton.start, automaton.start))

    # edges between nodes
    # first collect all labels for one edge
    store = collections.defaultdict(lambda: [])

    for (k, v) in automaton.transitions.items():
        q = k[0]
        store[q, v].append(k[1])

    # then write it
    for (k, v) in store.items():
        sid = k[0]
        nsid = k[1]
        fd.write("  n%d -> n%d [label=\"%s\"];\n" % (sid, nsid, ','.join(format_ranges(v))))
    # trailer
    fd.write("}\n")
    
    
def export_graphviz_epsilon_nfa(automaton, fd):
    # header
    fd.write("digraph G {\n")
    fd.write("  rankdir=LR;\n")
    # content
    for s in range(automaton.states):
        if s in automaton.final:
            fd.write("  n%d [label=\"%d\",xlabel=\"%s\",shape=\"doublecircle\"];\n" % (s, s, automaton.final[s]))
            # fd.write("  n%d [label=\"%d\",shape=\"doublecircle\"];\n" % (s, s))
        else:
            fd.write("  n%d [label=\"%d\",shape=\"circle\"];\n" % (s, s))

    # dummy starts
    #for q in automaton.starts:
    fd.write("  START%d [shape=\"point\",color=\"white\",fontcolor=\"white\"];\n" % automaton.start)
    fd.write("  START%d -> n%d;\n" % (automaton.start, automaton.start))

    # edges between nodes
    # first collect all labels for one edge
    store = collections.defaultdict(lambda: [])

    for (q, a, p) in automaton.transitions:
        store[q, p].append(a)

    # then write it
    for (k, v) in store.items():
        sid = k[0]
        nsid = k[1]
        # print(list(x for x in _ranges(v)))
        fd.write("  n%d -> n%d [label=\"%s\"];\n" % (sid, nsid, ','.join(format_ranges(v))))
    # trailer
    fd.write("}\n")
    
def export_graphviz_thompson_nfa(automaton, fd):
    # header
    fd.write("digraph G {\n")
    fd.write("  rankdir=LR;\n")
    # content
    for s in range(automaton.states):
        if s == automaton.final:
            fd.write("  n%d [label=\"%d\",shape=\"doublecircle\"];\n" % (s, s))
        else:
            fd.write("  n%d [label=\"%d\",shape=\"circle\"];\n" % (s, s))

    # dummy start
    fd.write("  START%d [shape=\"point\",color=\"white\",fontcolor=\"white\"];\n" % automaton.start)
    fd.write("  START%d -> n%d;\n" % (automaton.start, automaton.start))

    # edges between nodes
    # first collect all labels for one edge
    store = collections.defaultdict(lambda: [])

    for (q, a, p) in automaton.transitions:
        store[q, p].append(a)

    # then write it
    for (k, v) in store.items():
        sid = k[0]
        nsid = k[1]
        # print(list(x for x in _ranges(v)))
        fd.write("  n%d -> n%d [label=\"%s\"];\n" % (sid, nsid, ','.join(format_ranges(v))))
    # trailer
    fd.write("}\n")