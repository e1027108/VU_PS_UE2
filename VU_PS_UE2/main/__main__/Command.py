'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from __main__ import Component
from __main__ import Expression

class Command(Component):
    
    def __init__(self,input):
        super().__init__(self,input)
    
    def checkSyntax(self):
        test = self.input.lstrip()
        test = test.rstrip() #removing leading then trailing whitespaces
        
        if test[0] is '[' and test[len(test)-1] is ']':
            return self.checkGuardPart(test[1:len(test)-2])
        elif test[0] is '^' and test[len(test)-1] is ';':
            e = Expression(test[1:len(test)-2]) #pass to Expression without '^' and ';'
            return e.checkSyntax()
        elif test[len(test)-1] is ';':
            return self.checkAssignmentPart(test[:len(test)-2])#TODO check in this method for '*'
        else:
            return False#TODO replace False with Exceptions? use boolean return type at all?
        
    def checkGuardPart(self,part):
        test = part.lstrip()
        test = test.rstrip()
        
        '''
        TODO since guard as well as expression can both contain ':'
        we can't just look for a ':', but rather we need to
        check every combination of x : y whether or not
        it passes syntax checks for guard : expression ???
        '''
        
        pass
        
    def checkAssignmentPart(self,part):
        test = part.lstrip()
        test = test.rstrip()
        noPointerIndex = 0
        
        equalsIndex = test.index('=') #returns index of leftmost '='
        
        for x in range(0,len(test)-1):
            if test[x] is '*':
                continue
            else:
                noPointerIndex = x
                break
        
        left = test[noPointerIndex:equalsIndex-1]
        
        right = test[equalsIndex+1:]
        e = Expression(right)
        
        return (self.checkNamePart(left) and e.checkSyntax())
    
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