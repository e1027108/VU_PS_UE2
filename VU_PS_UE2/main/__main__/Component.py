'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
#defines the base class from which block, command, expression and guard Inherit

import abc
from PropertyList import PropertyList
from StringList import StringList
from Block import Block

class Component(object):
    
    def __init__(self,input):
        self.input = input
        self.property_list = PropertyList()
    
    def setInput(self,input):
        self.input = input
    
    def getInput(self):
        return self.input
    
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
    
    def getPropertyList(self):
        return self.property_list
       
    def concatenate(self,op1,op2):
        tmp1 = None
        tmp2 = None
        returnValue = None
        
        if isinstance(op1,PropertyList) and isinstance(op2,PropertyList):
            return self.concatenatePropertyLists(op1,op2)
        else:
            if isinstance(op1,Block):
                op1.checkSyntax() #or should/is that (be) initiated somewhere else?
                tmp1 = op1.getPropertylist()
            if isinstance(op2,Block):
                op2.checkSyntax() #or should/is that (be) initiated somewhere else?
                tmp2 = op2.getPropertylist()
        
        if not(tmp1 == None):
            returnValue == tmp1
        else:
            returnValue == op1
            
        if not(tmp2 == None):
            self.concatenate(returnValue,tmp2)
        else:
            self.concatenate(returnValue,op2)
            
        return returnValue
        
    def concatenatePropertyLists(self,op1,op2):
        if not(isinstance(op1,StringList) and isinstance(op2,StringList)):
            newList = PropertyList()
            newList.addProperty(op1.getDict())
            newList.addProperty(op2.getDict())
            return newList
        elif isinstance(op1,StringList) and isinstance(op2,StringList):
            newString = StringList("")
            newString.update({"string":op1.getProperty("string").get("string")+op2.getProperty("string").get("string")})
        else:
            pass #TODO concatenate two PropertyLists not of same inheritance level