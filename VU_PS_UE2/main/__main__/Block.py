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
        
        if (test[0] is '{') and (test[len(test)-1] is '}'):
            c = Command(test[1:len(test)-2])#supposed to put though everything between {}
            return c.checkSyntax()
        else:
            return False