'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
#defines the base class from which block, command, expression and guard Inherit

import abc

class Component(object):
    def __init__(self,input):
        self.input = input
    
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