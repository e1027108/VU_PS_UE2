'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from Component import Component
from Expression import Expression
from Guard import Guard

class Command(Component):
    
    def __init__(self,input):
        super(Command,self).__init__(input)
    
    def checkSyntax(self):
        test = self.input.lstrip()
        test = test.rstrip()
        
        oBI = 0 #openBracketIndex
        oPNI = 0 #openPointerOrNameIndex
        oPI = 0 #openPrintIndexx
        openBrackets = 0
        
        # is there an easier way than this huge loop?
        for x in range(0,len(test)):
            if (oPI == 0) and (oPNI == 0) and (oBI == 0):
                if test[x] == '[':
                    oBI = x
                    openBrackets += 1
                elif test[x] == '^':
                    oPI = x
                elif (test[x] == '*') or (test[x] == '"') or (test[x] == '(') or test[x].isalpha():#TODO check
                    oPNI = x
                elif (test[x] == '{'):#TODO check
                    oPNI = x
                    openBrackets += 1
            elif not (oBI == 0):
                if test[x] == '[':
                    openBrackets += 1
                elif test[x] == ']':
                    if openBrackets == 1:
                        if not self.checkGuardPart(test[oBI:x]):
                            return False
                        else:
                            oBI = 0
                    openBrackets -= 1
            elif not (oPI == 0):
                if test[x] == '{':
                    openBrackets += 1
                elif test[x] == '}':
                    openBrackets -= 1
                elif (openBrackets == 0) and (test[x] == ';'):
                    e = Expression(test[oPI:x])
                    if not e.checkSyntax():
                        return False
                    else:
                        oPI = 0
            elif not (oPNI == 0):
                if test[x] == '{':
                    openBrackets += 1
                elif test[x] == '}':
                    openBrackets -= 1
                elif (openBrackets == 0) and (test[x] == ';'):
                    e = Expression(test[oPNI:x])
                    if not e.checkSyntax():
                        return False
                    else:
                        oPNI = 0              
                
        return True
        
        ''' old code:
        if test[0] == '[' and test[len(test)-1] == ']':
            return self.checkGuardPart(test[1:len(test)-1])
        elif test[0] == '^' and test[len(test)-1] == ';':
            e = Expression(test[1:len(test)-1])
            return e.checkSyntax()
        elif test[len(test)-1] == ';':
            return self.checkAssignmentPart(test[:len(test)-1])
        else:
            return False #TODO replace False with Exceptions? use boolean return type at all?
        '''
        
    def checkGuardPart(self,part):
        test = part.lstrip()
        test = test.rstrip()
        openGuardCount = 0
        colonIndex = -1
        
        for x in range(0,len(test)):
            if (x == ':') and (openGuardCount == 0):
                colonIndex = x
                break
            elif x == '[':
                openGuardCount += 1
            elif x == ']':
                openGuardCount -= 1
                
        if colonIndex == -1:
            return False
        
        g = Guard(test[:colonIndex])
        c = Command(test[colonIndex+1:])
        
        return (g.checkSyntax() and c.checkSyntax())
        
    def checkAssignmentPart(self,part):
        test = part.lstrip()
        test = test.rstrip()
        noPointerIndex = 0
        
        equalsIndex = test.index('=') #returns index of leftmost '='
        
        for x in range(0,len(test)):
            if test[x] == '*':
                continue
            else:
                noPointerIndex = x
                break
        
        left = test[noPointerIndex:equalsIndex]
        
        right = test[equalsIndex+1:]
        e = Expression(right)
        
        if e.checkSyntax() and (self.checkName(left) or (equalsIndex == -1)):
            return True
        else:
            return False