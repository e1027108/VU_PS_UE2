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
        test = part.strip()
        
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
    
    def concatenate(self,op1,op2,stars):
        
        from Block import Block
        
        tmp = None
       
        if (len(op2.getDict()) == 1) and (self.isBlock(op2.getDict().values()[0])):
            if (len(op1.getDict()) == 1) and (self.isBlock(op1.getDict().values()[0])):
                raise KeyError
            tmp = op2.getDict().values()[0]
            
            if isinstance(self,Block):
                newBlock = Block(tmp,self)
            else:
                newBlock = Block(tmp,self.getParent())
                
            newBlock.setPropertyList(op1)
            newBlock.setSyntaxOnly(self.syntax_only)
            newBlock.setNested(stars)
            newBlock.checkSyntax()
            return newBlock.getPropertyList()
        else:
            return self.concatenatePropertyLists(op1, op2)
        
    def concatenatePropertyLists(self,op1,op2):
        if not(isinstance(op1,StringList)) and not(isinstance(op2,StringList)):
            newList = PropertyList()
            newList.getDict().update(op1.getDict())
            newList.getDict().update(op2.getDict())
            return newList
        elif isinstance(op1,StringList) and isinstance(op2,StringList):
            newString = StringList("")
            newString.changeProperty("string",op1.getProperty("string")+op2.getProperty("string"))
            return newString
        else:
            tmp = StringList("")
            if isinstance(op1,StringList):
                tmp.getDict().update(op2.getDict())
                tmp.changeProperty("string",op1.getProperty("string"))
            else:
                tmp.getDict().update(op1.getDict())
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
    
    def isBlock(self,potentialBlock):
        if (isinstance(potentialBlock,basestring) and len(potentialBlock) > 0):            
            if (potentialBlock[0] == '{' and potentialBlock[len(potentialBlock)-1] == '}'):
                return True
        else:
            return False