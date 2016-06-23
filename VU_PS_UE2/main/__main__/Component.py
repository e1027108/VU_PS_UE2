'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
#defines the base class from which block, command, expression and guard Inherit

import abc

class Component(object):
    def __init__(self,input):
        self.__input = input
    
    @input.setter
    def setInput(self,input):
        self.__input = input
       
    @input.getter 
    def getInput(self):
        return self.__input
    
    @abc.abstractmethod
    def checkSyntax(self):
        return
    
    def checkName(self,part):
        test = part.lstrip()
        test = test.rstrip()
        
        if not (test[0].isalpha()):
            return False
        else:
            for x in range(1,len(test)):
                if not (test[x].isalpha() or test[x].isdigit()):
                    return False
                
        return True