'''
Created on 21. Juni 2016

@author: raidsnail
'''
from __main__ import Component
from __main__ import Expression

class Guard(Component):
    
    def __init__(self,input):
        super().__init__(self,input)
    
    def checkSyntax(self):
        
        test = self.input.lstrip()
        test = test.rstrip()
             
        expIndex = 0
        guardIndex = 0
        
               
        for x in range(0, len(str)):
            if ((x == '=') or (x == '#')):
                e1 = Expression(test[:x-1])
                expIndex = x+1
            elif (x == ','):
                e2 = Expression(test[expIndex:x-1])
                guardIndex = x+1
                
        if(expIndex == 0):
            return False
                
        if(guardIndex == 0):
            e2 = Expression(test[expIndex:])
            return (e1.checkSyntax() and e2.checkSyntax())
        else:
            g = Guard(test[guardIndex:])
            return (e1.checkSyntax() and e2.checkSyntax() and g.checkSyntax())
        
        
        
        