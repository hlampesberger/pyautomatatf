'''
Created on 18. Aug. 2016

@author: P24667
'''
from regex.multiregex import MultiRegex


if __name__ == '__main__':
    reg1 = MultiRegex([r"^abb*c$"])
    reg2 = MultiRegex([r"^ab+c$"])
    reg3 = MultiRegex([r"^ab+c"])
    reg4 = MultiRegex([r"ab+c$"])
    
    assert(reg1.dfa == reg2.dfa)
    assert(reg1.dfa != reg3.dfa)
    assert(reg2.dfa != reg4.dfa)
    