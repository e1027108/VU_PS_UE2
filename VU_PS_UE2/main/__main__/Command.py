'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from __main__ import Component
from __main__ import Expression
from __main__ import Guard

class Command(Component):
    
    def __init__(self,input):
        super().__init__(self,input)
    
    def checkSyntax(self):
        test = self.input.lstrip()
        test = test.rstrip() #removing leading then trailing whitespaces
        
        if test[0] is '[' and test[len(test)-1] is ']':
            return self.checkGuardPart(test[1:len(test)-1])
        elif test[0] is '^' and test[len(test)-1] is ';':
            e = Expression(test[1:len(test)-1]) #pass to Expression without '^' and ';'
            return e.checkSyntax()
        elif test[len(test)-1] is ';':
            return self.checkAssignmentPart(test[:len(test)-1])#TODO check in this method for '*'
        else:
            return False #TODO replace False with Exceptions? use boolean return type at all?
        
    def checkGuardPart(self,part):
        test = part.lstrip()
        test = test.rstrip()
        openGuardCount = 0
        colonIndex = -1
        
        for x in range(0,len(test)):
            if (x is ':') and (openGuardCount == 0):
                colonIndex = x
                break
            elif x is '[':
                openGuardCount += 1
            elif x is ']':
                openGuardCount -= 1
                
        if colonIndex == -1:
            return False
        
        g = Guard(test[:colonIndex])
        e = Expression(test[colonIndex+1:])
        
        return (g.checkSyntax() and e.checkSyntax())
        
    def checkAssignmentPart(self,part):
        test = part.lstrip()
        test = test.rstrip()
        noPointerIndex = 0
        
        equalsIndex = test.index('=') #returns index of leftmost '='
        
        for x in range(0,len(test)):
            if test[x] is '*':
                continue
            else:
                noPointerIndex = x
                break
        
        left = test[noPointerIndex:equalsIndex]
        
        right = test[equalsIndex+1:]
        e = Expression(right)
        
        if e.checkSyntax() and (self.checkNamePart(left) or (equalsIndex == -1)):
            return True
        else:
            return False
    
    def checkNamePart(self,part):
        test = part.lstrip()
        test = test.rstrip()
        
        if not (test[0].isalpha()):
            return False
        else:
            for x in range(1,len(test)):
                if not (test[x].isalpha() or test[x].isdigit()):
                    return False
                
        return True