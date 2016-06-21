'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from __main__ import Component
from __main__ import Command

class Block(Component):
    
    def __init__(self,input):
        super().__init__(self,input)
    
    def checkSyntax(self): #no clue how to deal with comments like this code to interpret yet
        for x in range(0,len(self.input)-1):
            if input[x] is ' ':
                continue
            elif input[x] is '{':
                open = x
                break
            else:
                return False
        
        for x in range(len(self.input)-1,0,-1):#supposed to count -1 each step now
            if input[x] is ' ':
                continue
            elif input[x] is '}':
                close = x
                break
            else:
                return False
        
        c = Command(self.input[open+1:close-1])#supposed to put though everything between {}
        return c.checkSyntax()