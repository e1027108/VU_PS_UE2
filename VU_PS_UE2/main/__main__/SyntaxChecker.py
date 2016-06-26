'''
Created on 26. Juni 2016

@author: patrick.bellositz
'''

from CommentRemover import removeComments
from Block import Block

def checkSyntax(path):
    with open (path, "r") as myfile:
        data=myfile.read()
    
    #print data

    data = removeComments(data)

    #TODO now check Syntax
    
    b = Block(data)
    
    return b.checkSyntax()