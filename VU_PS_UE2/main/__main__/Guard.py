'''
Created on 21. Juni 2016

@author: raidsnail
'''
from Component import Component
from Expression import Expression

class Guard(Component):
    
    def __init__(self,input):
        super(Guard,self).__init__(input)
        
    def checkSyntax(self):
        
        test = self.input.lstrip()
        test = test.rstrip()
        
        stringOpen = False
        blockOpen = False
        expOpen = False 
        
        blockOpenCounter = 0
        blockCloseCounter = 0
        
        expOpenCounter = 0
        expCloseCounter = 0
             
        expIndex = 0
        guardIndex = 0
        
        equals = False
        not_equals = False
        
               
        for x in range(0, len(test)):
            if (test[x] == '"'):
                if (stringOpen == False):
                    stringOpen = True
                else:
                    stringOpen = False
            if (test[x] == '{'):
                if(blockOpenCounter == 0):
                    blockOpen = True
                blockOpenCounter += 1
            if (test[x] == '}'):
                blockCloseCounter += 1
                if (blockOpenCounter == blockCloseCounter):
                    blockOpen = False
            if (test[x] == '('):
                if(expOpenCounter == 0):
                    expOpen = True
                expOpenCounter += 1
            if (test[x] == ')'):
                expCloseCounter += 1
                if(expCloseCounter == expOpenCounter):
                    expOpen = False
            if (stringOpen == False and blockOpen == False and expOpen == False):
                if (expIndex == 0 and ((test[x] == '=') or (test[x] == '#'))):
                    if(test[x] == '='):
                        equals = True
                    if(test[x] == '#'):
                        not_equals = False
                    e1 = Expression(test[:x-1])
                    expIndex = x+1
                elif (test[x] == ','):
                    if (expIndex == 0):
                        print ("Missing expression in Guard-Command: " + test + "\nPlease check correct Syntax: expression ('='|'#') expression [',' guard]")
                        return False
                    e2 = Expression(test[expIndex:x])
                    guardIndex = x+1
                    break
                    
        if(expIndex == 0):
            print ("Missing '=' or '#' found in Guard-Command: " + test + "\nPlease check correct Syntax: expression ('='|'#') expression [',' guard]")
            return False
                
        if(guardIndex == 0):
            e2 = Expression(test[expIndex:])
            if(e1.checkSyntax() and e2.checkSyntax()):
                if(equals):
                    if(e1.getInput() == e2.getInput()):
                        return True
                if(not_equals):
                    if(e1.getInput() != e2.getInput()):
                        return True
                return False
            else:
                return False
        else:
            g = Guard(test[guardIndex:])
            if(e1.checkSyntax() and e2.checkSyntax()):
                if(equals):
                    if(e1.getInput() == e2.getInput()):
                        return g.checkSyntax()
                if(not_equals):
                    if(e1.getInput() != e2.getInput()):
                        return g.checkSyntax()
                return False
            else:
                return False
        
        
        
        