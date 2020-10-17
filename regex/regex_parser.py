'''
Created on 25.09.2014

@author: harald

Original perl RE semantics specified in pyparsing
From http://web.archive.org/web/20090129224504/http://faqts.com/knowledge_base/view.phtml/aid/25718/fid/200
'''

from pyparsing import Literal, Word, alphanums, Optional, \
    Forward, ParseBaseException
import pyparsing
import sys

# import part3_regex.graphviz_regex
from regex.regex import Esc, AnyCharacter, Alphanum, Meta, Character, Empty, \
    CharacterClass, Expression, Iteration, Eventually, Sequence, Choice, Atom, \
    Factor, RootExpression, Term, Plus


def _root_expression_helper(orig, loc, tok):
    if len(tok):
        anchor_left = False
        anchor_right = False
        center = tok[0]
        if tok[0] == '^':
            anchor_left = True
            center = tok[1]
        if tok[-1] == '$':
            anchor_right = True
        return RootExpression(center, anchor_left, anchor_right)
    else:
        raise RuntimeError("A rootExpression without any content is not possible!")


class RegexParser(object):
    esc = r"(){}[]*|+^$/.?tnrf-"
    hex = r"0123456789ABCDEFabcdef"
    # defined by pyparsing    
    # alphanums = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789

    alphanum = Word(alphanums, exact=1)
    alphanum.leaveWhitespace()
    alphanum.setParseAction(lambda orig, loc, tok: Alphanum(tok[0]))
 
    meta = Word(r" \#!\"%§&'/,:;<=>@_-~", exact=1)
    meta.leaveWhitespace()
    meta.setParseAction(lambda orig, loc, tok: Meta(tok[0]))   
    
    anyCharacter = Literal('.')
    anyCharacter.leaveWhitespace()
    anyCharacter.setParseAction(lambda orig, loc, tok: AnyCharacter(tok[0]))
    
    escapedCharacter = Literal('\\\\') | Literal('\\x') + Word(hex, exact=2) | Literal('\\') + Word(esc, exact=1)
    escapedCharacter.leaveWhitespace()
    escapedCharacter.setParseAction(lambda orig, loc, tok: Esc(''.join(tok)))

    character = escapedCharacter | alphanum | meta
    character.leaveWhitespace()
    character.setParseAction(lambda orig, loc, tok: Character(tok[0]))
    
    characterClass = Literal('[') + pyparsing.OneOrMore(escapedCharacter | alphanum | meta) + Literal(']')
    characterClass.leaveWhitespace()
    characterClass.setParseAction(lambda orig, loc, tok: CharacterClass(tok[1:-1]))
    
    expression = Forward()
    
    atom = anyCharacter | characterClass | character | Literal('(').suppress() + expression + Literal(')').suppress()
    atom.leaveWhitespace()
    atom.setParseAction(lambda orig, loc, tok: Atom(tok[0]))

    eventually = atom + Literal('?')
    eventually.leaveWhitespace()
    eventually.setParseAction(lambda orig, loc, tok: Eventually(tok[0]))

    iteration = atom + Literal('*')
    iteration.leaveWhitespace()
    iteration.setParseAction(lambda orig, loc, tok: Iteration(tok[0]))

    plus = atom + Literal('+')
    plus.leaveWhitespace()
    plus.setParseAction(lambda orig, loc, tok: Plus(tok[0]))

    factor = iteration | plus | eventually | atom
    factor.leaveWhitespace()
    factor.setParseAction(lambda orig, loc, tok: Factor(tok[0]))

    term = Forward()
    
    sequence = factor + term
    sequence.leaveWhitespace()
    sequence.setParseAction(lambda orig, loc, tok: Sequence(tok[0], tok[1]))

    term << (sequence | factor)
    term.leaveWhitespace()
    term.setParseAction(lambda orig, loc, tok: Term(tok[0]))
    
    choice = term + Literal('|') + expression
    choice.leaveWhitespace()
    choice.setParseAction(lambda orig, loc, tok: Choice(tok[0], tok[2]))

    empty = pyparsing.Empty()
    empty.leaveWhitespace()
    empty.setParseAction(lambda orig, loc, tok: Empty())

    expression << (choice | term | empty)
    expression.leaveWhitespace()
    expression.setParseAction(lambda orig, loc, tok: Expression(tok[0]))
 
    rootExpression = Optional(Literal('^')) + expression + Optional(Literal('$'))
    rootExpression.leaveWhitespace()
    rootExpression.setParseAction(_root_expression_helper)
 
    @classmethod
    def parse(cls, strng):
        if not isinstance(strng, str):
            raise Exception("Method parse() expects a string, however the argument is of type %s!" % strng.__class__.__name__)
        try:
            # temporarily limit traceback, otherwise it will flood the tests
            sys.tracebacklimit = 3
            return cls.rootExpression.parseString(strng, parseAll=True)[0]
            sys.tracebacklimit = 1000
        except ParseBaseException as exc:
            raise exc



