'''
Created on 23. Juni 2016

@author: patrick.bellositz
'''

def removeComments(input):
    commentIndex = -1
    openQuote = 0
    
    for x in range(0,len(input)):
        if (input[x] == '"') and commentIndex == -1:
            if openQuote == 0:
                openQuote = 1
            elif openQuote == 1:
                openQuote = 0
        if (input[x] == '%') and (commentIndex == -1) and openQuote == 0 :
            commentIndex = x
        elif (input[x] == '\n') and not (commentIndex == -1):
            input = input.replace(input[commentIndex:x],"")
            input = input[:commentIndex+1] + removeComments(input[commentIndex+1:])
            break
    
    return input

#string = "test test test %test test 3 4 5\n test again again again%comment more comment more 2 3 4\n testing ends"
#print removeComments(string)