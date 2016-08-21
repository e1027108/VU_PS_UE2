'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
#defines the base class from which block, command, expression and guard Inherit

import abc
from PropertyList import PropertyList
from StringList import StringList

class Component(object):
    
    def __init__(self,input,parent):
        self.input = input
        self.parent = parent # meaning the parent block
        self.property_list = PropertyList()
        self.syntax_only = False
    
    def setInput(self,input):
        self.input = input
    
    def getInput(self):
        return self.input
    
    def getParent(self):
        return self.parent
    
    def getSyntaxOnly(self):
        return self.syntax_only
    
    def setSyntaxOnly(self,newvalue):
        self.syntax_only = newvalue
    
    @abc.abstractmethod
    def checkSyntax(self):
        pass
    
    def checkName(self,part):
        test = part.lstrip()
        test = test.rstrip()
        
        if not (test[0].isalpha()):
            print "'" + test[0] + "' is not a letter. It can not be at the beginning of a name."
            return False
        else:
            for x in range(1,len(test)):
                if not (test[x].isalpha() or test[x].isdigit()):
                    print "'" + test[x] + "' is neither letter nor digit. It can not be part of a name."
                    return False
                
        return True
    
    def setPropertyList(self,list):
        self.property_list = list 
    
    def getPropertyList(self):
        return self.property_list
    
    '''
        TODO check whether this is working as intended, especially check:
        The left-hand side of + is executed first (starting with a new empty property list),
        the right-hand side afterward (starting with the result of applying the left-hand side).  
    '''
    def concatenate(self,op1,op2):
        
        from Block import Block
        
        tmp1 = None
        tmp2 = None
        returnValue = None
               
        if isinstance(op1,PropertyList) and isinstance(op2,PropertyList):
            return self.concatenatePropertyLists(op1,op2)
        else:
            if isinstance(op1,Block):
                tmp1 = op1.getPropertyList()
            if isinstance(op2,Block):
                tmp2 = op2.getPropertyList()
        
        if not(tmp1 == None):
            returnValue = tmp1
        else:
            returnValue = op1
            
        if not(tmp2 == None):
            self.concatenate(returnValue,tmp2)
        else:
            self.concatenate(returnValue,op2)
            
        return returnValue
        
    def concatenatePropertyLists(self,op1,op2):
        if not(isinstance(op1,StringList)) and not(isinstance(op2,StringList)):
            newList = PropertyList()
            newList.getDict().update(op1.getDict())
            newList.getDict().update(op2.getDict())
            return newList
        elif isinstance(op1,StringList) and isinstance(op2,StringList):
            newString = StringList("")
            ######newString.changeProperty("string",op1.getProperty("string").get("string")+op2.getProperty("string").get("string"))
            newString.changeProperty("string",op1.getProperty("string")+op2.getProperty("string"))
            return newString
        else:
            tmp = StringList("")
            if isinstance(op1,StringList):
                tmp.getDict().update(op2.getDict())
                #tmp = op2
                ######tmp.addProperty("string",op1.getProperty("string").get("string"))
                tmp.changeProperty("string",op1.getProperty("string"))
            else:
                #tmp = op1
                tmp.getDict().update(op1.getDict())
                ######tmp.addProperty("string",op2.getProperty("string").get("string"))
                tmp.changeProperty("string",op2.getProperty("string"))
            return tmp
            
    def countStartOccurrences(self,text,char):
        count = 0
        for x in range(0,len(text)):
            if text[x] == char:
                count += 1
            else:
                break
        return count