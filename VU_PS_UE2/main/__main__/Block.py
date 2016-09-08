'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
from Component import Component
from Command import Command

class Block(Component):
    
    def __init__(self,input,parent):
        super(Block,self).__init__(input,parent)
        self.nested = 0
        
    def getNested(self):
        return self.nested
    
    #is this nested (0/1)?
    def setNested(self,nest):
        self.nested = nest
    
    def checkSyntax(self):
        test = self.getInput().strip()
        
        if (test[0] == '{') and (test[len(test)-1] == '}'):
            c = Command(test[1:len(test)-1],self) #supposed to put though everything between {}
            c.setSyntaxOnly(self.syntax_only)
            if not self.syntax_only:
                c.setPropertyList(self.property_list) #commands should get access to all already existing propertylists?
            if c.checkSyntax():
                if not self.syntax_only:
                    cList = c.getPropertyList().getDict()
                    sList = self.property_list.getDict()
                    sList.update(cList)
                return True
            else:
                return False
        else:
            print "The first symbol (currently '" + test[0] + ("') needs to be '{' and the last symbol "
                "(currently '") + test[len(test)-1] + "') needs to be '}'. Therefore the block is not valid."
            return False