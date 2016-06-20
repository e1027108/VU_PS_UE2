'''
Created on 20. Juni 2016

@author: patrick.bellositz
'''
#defines the base class from which block, command, expression and guard Inherit

import abc

class Component():
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