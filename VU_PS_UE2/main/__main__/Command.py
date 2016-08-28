'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from Component import Component
from Expression import Expression
from Guard import Guard
from StringList import StringList

class Command(Component):
    
    def __init__(self,input,parent):
        super(Command,self).__init__(input,parent)
    
    def checkSyntax(self):
        test = self.input.lstrip()
        test = test.rstrip()
        
        oBI = -1 #openBracketIndex
        oPNI = -1 #openPointerOrNameIndex
        oPI = -1 #openPrintIndexx
        openBrackets = 0
        qOpen = 0 #quotesOpen (yes/no)
        concluded = 1
        outerblock = 0
        
        # is there an easier way than this huge loop?
        for x in range(0,len(test)):
            if test[x] == '"': #we do not expect to find " within a string literal (no escape character detection)
                if qOpen == 1:
                    qOpen = 0
                else:
                    qOpen = 1
            
            if (oPI == -1) and (oPNI == -1) and (oBI == -1):
                if test[x] == '[':
                    oBI = x
                    openBrackets = self.manageBrackets(openBrackets,qOpen,1)
                elif test[x] == '^':
                    oPI = x
                    concluded = 0
                elif (test[x] == '*') or (test[x] == '"') or test[x].isalpha():
                    oPNI = x
                    concluded = 0
                elif (test[x] == '{') or (test[x] == '('):
                    oPNI = x
                    openBrackets = self.manageBrackets(openBrackets,qOpen,1)
                    concluded = 0
            elif not (oBI == -1):
                if test[x] == '[':
                    openBrackets = self.manageBrackets(openBrackets,qOpen,1)
                elif test[x] == ']':
                    if openBrackets == 1:
                        if not self.checkGuardPart(test[oBI:x+1]): # on true handling below
                            return False
                        else:       
                            oBI = -1
                    openBrackets = self.manageBrackets(openBrackets,qOpen,-1)
            elif not (oPI == -1):
                if test[x] == '{' or test[x] == '[' or test[x] == '(':
                    openBrackets = self.manageBrackets(openBrackets,qOpen,1)
                elif test[x] == '}' or test[x] == ']' or test[x] == ')':
                    openBrackets = self.manageBrackets(openBrackets,qOpen,-1)
                elif (openBrackets == 0) and (test[x] == ';'):
                    #print test[oPI+1:x]
                    e = Expression(test[oPI+1:x],self.getParent())
                    e.setSyntaxOnly(self.syntax_only)
                    if not e.checkSyntax():
                        return False
                    else:
                        if(not e.getSyntaxOnly()):
                            self.property_list = e.getPropertyList()
                            self.getParent().setSyntaxOnly(True)
                        return True # terminating the execution of the block
            elif not (oPNI == -1):
                if test[x] == '{' or test[x] == '[' or test[x] == '(':
                    openBrackets = self.manageBrackets(openBrackets,qOpen,1)
                elif test[x] == '}' or test[x] == ']' or test[x] == ')':
                    openBrackets = self.manageBrackets(openBrackets,qOpen,-1)
                elif (openBrackets == 0) and (test[x] == ';'):
                    namelength = 0
                    if(test[oPNI] == '*' or test[oPNI].isalpha()):
                        if(not self.syntax_only):
                            outerblock = self.countStartOccurrences(test[oPNI:],'*')
                        if '=' in test[oPNI:]:
                            namelength = test[oPNI:].index('=')+1
                    expressionString = test[oPNI+namelength:x].strip()
                    e = Expression(expressionString,self.getParent())
                    if (self.isBlock(expressionString)):
                        e.setSyntaxOnly(True)
                    else:
                        e.setSyntaxOnly(self.syntax_only)
                    if not e.checkSyntax():
                        return False
                    else:
                        if(not self.syntax_only):
                            curr = self.getParent()
                            for x in range (0,outerblock):
                                curr = curr.getParent()
                            
                            name = test[oPNI:oPNI+namelength-1].strip()
                        
                            if curr == self.getParent():
                                if(namelength != 0 and self.isBlock(expressionString)): #must have found an assignment
                                    curr.getPropertyList().addProperty(name,expressionString)
                                else:
                                    curr.getPropertyList().addProperty(name,e.getPropertyList())
                            else:
                                if(namelength != 0 and self.isBlock(expressionString)):
                                    curr.getPropertyList().changeProperty(name,expressionString)
                                else:
                                    curr.getPropertyList().changeProperty(name,e.getPropertyList())
                        
                            outerblock = 0
                        
                        oPNI = -1
                        concluded = 1  
        
        if openBrackets > 0:
            print "There are " + str(openBrackets) + " unclosed brackets in:\n" + test + "\nIt is not a valid list of commands."
            return False
        elif concluded == 0:
            print "There is an unfinished command in:\n"  + test + "\nA ';' is missing."
            return False
          
        return True
        
    def manageBrackets(self,openb,quotes,v): #TODO find out what v does again
        if(quotes==0):
            return (openb+v)
        else:
            return openb
        
    def checkGuardPart(self,part):        
        test = part.strip()
        openGuardCount = 0
        colonIndex = -1
        qOpen = 0
        
        for x in range(0,len(test)):
            if test[x] == '"':
                if qOpen == 1:
                    qOpen = 0
                else:
                    qOpen = 1
            
            if (test[x] == ':') and (openGuardCount == 1):
                if not (colonIndex == -1):
                    print "Only one ':' is allowed, invalid command: " + test
                    return False
                colonIndex = x
            elif test[x] == '[':
                openGuardCount = self.manageBrackets(openGuardCount, qOpen, 1)
            elif test[x] == ']':
                openGuardCount = self.manageBrackets(openGuardCount, qOpen, -1)
                
        if colonIndex == -1:
            print "Not a guard command: " + test + " is missing ':'."
            return False
        
        g = Guard(test[1:colonIndex],self.getParent())
        c = Command(test[colonIndex+1:len(test)-1],self.getParent())
        
        guardValue = g.checkSyntax()
        
        if guardValue == -1: #syntax problem
            return False
        elif guardValue == 0: #semantically wrong i.e. the "program" guard returns false
            c.setSyntaxOnly(True)
            return c.checkSyntax()
        elif guardValue == 1: #check
            return c.checkSyntax()