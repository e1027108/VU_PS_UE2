'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from __main__ import Component
from __main__ import Command

class Block(Component):
    
    def __init__(self,input):
        super().__init__(self,input)
    
    def checkSyntax(self): #no clue how to deal with comments (like this) yet
        test = self.input.lstrip()
        test = test.rstrip()
        
        if (test[0] == '{') and (test[len(test)-1] == '}'):
            c = Command(test[1:len(test)-1])#supposed to put though everything between {}
            return c.checkSyntax()
        else:
            return False