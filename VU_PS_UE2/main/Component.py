'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
#defines the base class from which block, command, expression and guard Inherit

import abc

class Component():
    inputString = "" #here we want to get the input
    
    @inputString.setter
    def setInput(self,input):
        self.inputString = input
       
    @inputString.getter 
    def getInput(self):
        return self.inputString
    
    @abc.abstractmethod
    def checkSyntax(self):
        return