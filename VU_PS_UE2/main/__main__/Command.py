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
        
        oBI = -1 #openBracketIndex
        oPNI = -1 #openPointerOrNameIndex
        oPI = -1 #openPrintIndexx
        openBrackets = 0
        
        # is there an easier way than this huge loop?
        for x in range(0,len(test)):
            if (oPI == -1) and (oPNI == -1) and (oBI == -1):
                if test[x] == '[':
                    oBI = x
                    openBrackets += 1
                elif test[x] == '^':
                    oPI = x
                elif (test[x] == '*') or (test[x] == '"') or test[x].isalpha():
                    oPNI = x
                elif (test[x] == '{') or (test[x] == '('):
                    oPNI = x
                    openBrackets += 1
            elif not (oBI == -1):
                if test[x] == '[':
                    openBrackets += 1
                elif test[x] == ']':
                    if openBrackets == 1:
                        if not self.checkGuardPart(test[oBI:x]):
                            return False
                        else:
                            oBI = -1
                    openBrackets -= 1
            elif not (oPI == -1):
                if test[x] == '{' or test[x] == '[' or test[x] == '(':
                    openBrackets += 1
                elif test[x] == '}' or test[x] == ']' or test[x] == ')':
                    openBrackets -= 1
                elif (openBrackets == 0) and (test[x] == ';'):
                    e = Expression(test[oPI:x])
                    if not e.checkSyntax():
                        return False
                    else:
                        oPI = -1
            elif not (oPNI == -1):
                if test[x] == '{' or test[x] == '[' or test[x] == '(':
                    openBrackets += 1
                elif test[x] == '}' or test[x] == ']' or test[x] == ')':
                    openBrackets -= 1
                elif (openBrackets == 0) and (test[x] == ';'):
                    if(test[oPNI] == '*' or test[oPNI].isalpha()):
                        oPNI += test[oPNI:].index('=')+1
                    #print test[oPNI:x]
                    e = Expression(test[oPNI:x])
                    if not e.checkSyntax():
                        return False
                    else:
                        oPNI = -1            
                
        return True
        
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