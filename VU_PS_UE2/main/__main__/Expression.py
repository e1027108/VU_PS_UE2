'''
Created on 21. Juni 2016

@author: raidsnail
'''
from __main__ import Component
from __main__ import Block

class Expression(Component):
    
    def __init__(self,input):
        super().__init__(self,input)
    
    def checkSyntax(self):
        
        test = self.input.lstrip()
        test = test.rstrip()
        
        nameIndex = 0
        expIndex = 0
        
        part1 = test
        
        for x in range(0, len(test)):
            if (x =='.'):
                # this is a name starting with .
                if(nameIndex == 0):
                    part1 = test[:x-1]
                nameIndex = x+1;
            elif(x == '+' and expIndex == 0):
                # optional expression
                e = Expression(test[x+1:])
                if(nameIndex == 0):
                    part1 = test[:x-1]
                expIndex = x+1;
                
        

        if (expIndex == 0):
            return (self.checkPart1(test))     
        else:
            return (self.checkPart1(part1) and e.checkSyntax())
        
        return False
    
        ## missing .name and *name handling!!!

        
    def checkPart1(self, test):
        
        if (test[0] == '"' and test[len(test)-1]):
            return self.checkStringLiteral(test)
        elif (test[0] == '{' and test[len(test)-1] == '}'):
            b = Block(test[1:len(test)-1])
            return b.checkSyntax()
        elif (test[0] == '(' and test[len(test)-1] == ')'):
            e = Expression(test[1:len(test)-1])
            return e.checkSyntax()
        else:
            # this is a name with none or multiple *
            pass
        
        return False
        