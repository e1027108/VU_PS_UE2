'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from Component import Component
from Command import Command

class Block(Component):
    
    def __init__(self,input):
        super(Block,self).__init__(input)
    
    def checkSyntax(self):
        test = self.getInput().lstrip()
        test = test.rstrip()
        
        if (test[0] == '{') and (test[len(test)-1] == '}'):
            c = Command(test[1:len(test)-1]) #supposed to put though everything between {}
            c.setPropertyList(self.property_list) #commands should get access to all already existing propertylists?
            if c.checkSyntax():
                cList = c.getPropertyList().getDict()
                sList = self.property_list.getDict()
                for prop in cList:
                    sList.add(prop)
                return True
            else:
                return False
        else:
            print "The first symbol (currently '" + test[0] + ("') needs to be '{' and the last symbol "
                "(currently '") + test[len(test)-1] + "') needs to be '}'. Therefore the block is not valid."
            return False