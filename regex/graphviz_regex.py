'''
Created on 30.11.2014

@author: harald
'''

import os
import re
import subprocess
import tempfile

from regex.regex import RootExpression, Terminal, UnaryRegex, BinaryRegex

####### only use function 'draw_parsetree' from this file! #########
__all__ = ['draw_parsetree']

def _formatter(reg):
    if isinstance(reg, str): return reg
    elif isinstance(reg, RootExpression):
        return "%s(%s, %s)" % (reg.__class__.__name__, reg.anchor_left, reg.anchor_right)
    else: return reg.__class__.__name__

def _chooser(reg, node_id):
    if isinstance(reg, Terminal):
        yield reg.value, node_id + '0'
    elif isinstance(reg, UnaryRegex):
        yield reg.child, node_id + '0'
    elif isinstance(reg, BinaryRegex):
        yield reg.left, node_id + '0'
        yield reg.right, node_id + '1'
    elif isinstance(reg, list):
        for i, elem in enumerate(reg):
            yield elem, node_id + str(i)


def _gv(regex, node_id='0', parent_node_id=''):
    yield "  n%s [label=\"%s\", shape=\"none\"];\n" % (node_id, re.escape(_formatter(regex)))
    if parent_node_id != '':
        yield "  n%s -> n%s;\n" % (parent_node_id, node_id)
    for child, child_id in _chooser(regex, node_id):
        for node_data in _gv(child, child_id, node_id):
            yield node_data

def _export_graphviz(regex, fd):
    # header
    fd.write("digraph G {\n")
    fd.write("  rankdir=TB;\n")
    # content
    for line in _gv(regex):
        fd.write(line)
        #print(line)
    # trailer
    fd.write("}\n")
    
def draw_parsetree(obj, path):
    (fd, filename) = tempfile.mkstemp()
    try:
        tfile = os.fdopen(fd, "w")
        _export_graphviz(obj, tfile)
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
