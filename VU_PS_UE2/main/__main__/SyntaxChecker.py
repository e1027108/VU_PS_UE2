'''
Created on 26. Juni 2016

@author: patrick.bellositz
'''

from CommentRemover import removeComments
from Block import Block

def check(path,syntaxOnly):
    with open (path, "r") as myfile:
        data=myfile.read()

    data = removeComments(data)

    #TODO now check Syntax
    
    b = Block(data,None)
    b.setSyntaxOnly(syntaxOnly)
    
    return b.checkSyntax()

def checkSyntax(path):
    return check(path,False)

def checkSyntaxOnly(path):
    return check(path,True)