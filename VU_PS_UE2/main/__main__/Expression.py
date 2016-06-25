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
        
        stringOpen = False
        blockOpen = False
        expOpen = False 
        
        blockOpenCounter = 0
        blockCloseCounter = 0
        
        expOpenCounter = 0
        expCloseCounter = 0
        
        names = True
        
        part1 = test
        
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
                if (test[x] == '.'):
                    # this is a name starting with .
                    if (nameIndex == 0):
                        part1 = test[nameIndex:x]
                    part2 = test[x+1:]
                    if "." in part2:
                        dotIndex = part2.find(".")
                        part2 = part2[:dotIndex]
                    names = self.checkName(part2)
                    nameIndex = x+1;
                elif(test[x] == '+' and expIndex == 0):
                    # optional expression
                    e = Expression(test[x+1:])
                    if(nameIndex == 0):
                        part1 = test[:x-1]
                    expIndex = x+1;
                    break       
        
        if (expIndex == 0):
            return (self.checkPart1(part1) and names)     
        else:
            return (self.checkPart1(part1) and names and e.checkSyntax())
        
        return False

        
    def checkPart1(self, test):
        
        if (test[0] == '"' and test[len(test)-1] == '"'):
            # this is a string literal
            return self.checkStringLiteral(test)
        elif (test[0] == '{' and test[len(test)-1] == '}'):
            # this is a block
            b = Block(test[1:len(test)-1])
            return b.checkSyntax()            
        elif (test[0] == '(' and test[len(test)-1] == ')'):
            # this is an expression
            e = Expression(test[1:len(test)-1])
            return e.checkSyntax()
        else:
            # this is a name with none or multiple *
            return self.checkAsterix(test)    
        return False
    
    def checkStringLiteral(self, test):
        
        test = test[1:len(test)-1]
        k = '"'
               
        if k in test:
            return False
        
        return True
    
#     def checkName(self, part):
#         test = part.lstrip()
#         test = test.rstrip()
#         
#         if not (test[0].isalpha()):
#             return False
#         else:
#             for x in range(1,len(test)):
#                 if not (test[x].isalpha() or test[x].isdigit()):
#                     return False
#                 
#         return True
    
    def checkAsterix(self, part):
        test = part.lstrip()
        test = test.rstrip()
        
        nameIndex = 0
        otherIndex = len(test)
                
        for x in range(0, len(test)):
            if (test[x] == '*'):
                nameIndex +=1
            elif ((test[x] == '.' or test[x] == '+') and otherIndex == len(test)):
                otherIndex = x-1
                break
       
        if(otherIndex != len(test)):
            return self.checkName(test[nameIndex:otherIndex])
        
        return self.checkName(test[nameIndex:])
        