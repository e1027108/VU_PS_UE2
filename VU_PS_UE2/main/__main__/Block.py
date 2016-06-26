'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from Component import Component
from Command import Command

class Block(Component):
    
    def __init__(self,input):
        super(Block,self).__init__(input)
    
    def checkSyntax(self):
        test = self.getInput().lstrip()
        test = test.rstrip()
        
        if (test[0] == '{') and (test[len(test)-1] == '}'):
            c = Command(test[1:len(test)-1]) #supposed to put though everything between {}
            return c.checkSyntax()
        else:
            return False