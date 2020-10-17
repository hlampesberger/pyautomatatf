'''
Created on 24.11.2014

@author: hlampesberger
'''
""" Abstract classes for tree-structured Regex Parsetrees """

from abc import abstractmethod, ABCMeta

from automata.thompson_nfa import ThompsonNFA

class Regex(metaclass=ABCMeta):
    """ This metaclass enforces an 'eval' method in all derived classes 
        a Regex is a tree, where the leaves are strings from an original expression
        there are two kinds of non-leaf tree nodes: single child (unary), or two children (binary)"""
    @abstractmethod
    def eval(self): pass


class Terminal(Regex):
    """ An abstract class for Parsetree nodes representing a terminal character (0..255, or 256 for epsilon) """
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.value)) 

class UnaryRegex(Regex):
    """ An abstract class for Parsetree nodes with exactly one child """
    def __init__(self, child):
        self.child = child
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.child))

class BinaryRegex(Regex):
    """ An abstract class for Parsetree nodes with exactly two children """
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, repr(self.left), repr(self.right))      
    
    





""" Instantiable classes """

class Alphanum(Terminal):
    def eval(self):
        return ord(self.value)

class Meta(Terminal):
    def eval(self):
        return ord(self.value)

class Esc(Terminal):
    def eval(self):
        # escaping needs a little bit more treatment 
        # because of conflicting escape codes with the programming language
        if self.value.startswith("\\x"):
            # convert string after \x to integer
            val = int(self.value[2:], 16)
            assert(0 <= val <= 255)
            return val
        elif self.value == "\\\\":  return 92
        elif self.value == "\\t":  return 9
        elif self.value == "\\n":  return 10
        elif self.value == "\\f":  return 12
        elif self.value == "\\r":  return 13
        elif self.value[0] == "\\" and len(self.value) == 2: return ord(self.value[1])
        else: raise RuntimeError("Illegal Escape sequence recognized: %s", self.value) 


class Empty(Regex):
    def __init__(self):
        pass
    def __repr__(self):
        return self.__class__.__name__
    def eval(self):
        return ThompsonNFA.empty()

class Character(UnaryRegex):
    def eval(self):
        return ThompsonNFA.character(self.child.eval())

class AnyCharacter(UnaryRegex):
    def eval(self):
        return ThompsonNFA.wildcard()

class CharacterClass(UnaryRegex):
    def eval(self):
        character_set = {c.eval() for c in self.child}
        return ThompsonNFA.character_class(character_set)



class Iteration(UnaryRegex):
    def eval(self):
        #  ".*" compiler optimization to reduce number of epsilon transitions
        if isinstance(self.child, Atom) and isinstance(self.child.child, AnyCharacter):
            return ThompsonNFA.dotstar()
        else:
            return self.child.eval().iteration()

class Plus(UnaryRegex):
    def eval(self):
        #  ".+" compiler optimization to reduce number of epsilon transitions
        if isinstance(self.child, Atom) and isinstance(self.child.child, AnyCharacter):
            return ThompsonNFA.dotplus()
        else:
            return self.child.eval().plus()

class Eventually(UnaryRegex):
    def eval(self):
        return self.child.eval().eventually()
        
class Sequence(BinaryRegex):
    def eval(self):
        return self.left.eval().concat(self.right.eval())
    
class Choice(BinaryRegex):
    def eval(self):
        return self.left.eval().choice(self.right.eval())


class Expression(UnaryRegex):
    def eval(self):
        return self.child.eval()
class Atom(Expression): pass
class Factor(Expression): pass
class Term(Expression): pass
    
class RootExpression(UnaryRegex):
    def __init__(self, child, anchor_left, anchor_right):
        self.anchor_left = anchor_left
        self.child = child
        self.anchor_right = anchor_right
    def eval(self):
        ch = self.child.eval()
        if not self.anchor_left:
            ch = ThompsonNFA.dotstar().concat(ch)
        if not self.anchor_right:
            ch = ch.concat(ThompsonNFA.dotstar())
        return ch
    def __repr__(self):
        return "%s(%s, %s, %s)" % (self.__class__.__name__,
                                   repr(self.child),
                                   repr(self.anchor_left), repr(self.anchor_right))
    
  

