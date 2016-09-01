'''
Created on 21. Juni 2016

@author: raidsnail
'''
from Component import Component
from Expression import Expression

class Guard(Component):
    
    def __init__(self,input,parent):
        super(Guard,self).__init__(input,parent)
        
    def checkSyntax(self):
        
        test = self.input.lstrip()
        test = test.rstrip()
        
        stringOpen = False
        blockOpen = False
        expOpen = False 
        
        blockOpenCounter = 0
        blockCloseCounter = 0
        
        expOpenCounter = 0
        expCloseCounter = 0
             
        expIndex = 0
        guardIndex = 0
        
        equals = False
        not_equals = False
        
        for x in range(0, len(test)):
            if (test[x] == '"'):
                if (stringOpen == False):
                    stringOpen = True
                else:
                    stringOpen = False
            if (test[x] == '{'):
                if(blockOpenCounter == 0):
                    blockOpen = True
                blockOpenCounter += 1
            if (test[x] == '}'):
                blockCloseCounter += 1
                if (blockOpenCounter == blockCloseCounter):
                    blockOpen = False
            if (test[x] == '('):
                if(expOpenCounter == 0):
                    expOpen = True
                expOpenCounter += 1
            if (test[x] == ')'):
                expCloseCounter += 1
                if(expCloseCounter == expOpenCounter):
                    expOpen = False
            if (stringOpen == False and blockOpen == False and expOpen == False):
                if (expIndex == 0 and ((test[x] == '=') or (test[x] == '#'))):
                    if(test[x] == '='):
                        equals = True
                    if(test[x] == '#'):
                        not_equals = False
                    e1 = Expression(test[:x-1],self.getParent())
                    e1.setSyntaxOnly(self.syntax_only)
                    expIndex = x+2
                elif (test[x] == ','):
                    if (expIndex == 0):
                        print ("Missing expression in Guard-Command: " + test + "\nPlease check correct Syntax: expression ('='|'#') expression [',' guard]")
                        return -1
                    e2 = Expression(test[expIndex:x])
                    e2.setSyntaxOnly(self.syntax_only)
                    guardIndex = x+1
                    break
                    
        if(expIndex == 0):
            print ("Missing '=' or '#' found in Guard-Command: " + test + "\nPlease check correct Syntax: expression ('='|'#') expression [',' guard]")
            return -1
                
        if(guardIndex == 0):
            e2 = Expression(test[expIndex:],self.getParent())
            e2.setSyntaxOnly(self.syntax_only)
            g = Guard("",self.getParent())
            g.setSyntaxOnly(self.syntax_only)
        else:
            g = Guard(test[guardIndex:],self.getParent())
            g.setSyntaxOnly(self.syntax_only)
        
        if not self.syntax_only:
            return (self.checkSemantic(e1,e2,g,equals,not_equals))
        else:            
            if(g.getInput() != ""):
                if (e1.checkSyntax() and e2.checkSyntax() and g.checkSyntax()):
                    return 1
                else:
                    return -1
            else:
                if (e1.checkSyntax() and e2.checkSyntax()):
                    return 1
                else:
                    return -1
        
    def checkSemantic(self,e1,e2,g,equals,not_equals):
        
        from StringList import StringList
        
        #### wenn e2 ein stringliteral ist
        if(e1.checkSyntax() and e2.checkSyntax()):
            
            e1_comp_string = '""'
            e2_comp_string = '""'

            names = e1.getInput().split(".")
            if(len(e1.property_list.getDict()) > 0):
                if((len(e1.property_list.getDict()) == 1) and e1.property_list.exists("string")):
                    if(isinstance(e1.property_list.getProperty("string"), int)):
                        e1_comp_string = e1.property_list.getProperty("string")
                    elif(isinstance(e1.property_list.getProperty("string"),list)):
                        if(len(e1.property_list.getProperty("string")) > 0):
                            e1_comp_string = e1.property_list.getProperty("string")[0]
                else:
                    prop = e1.property_list.getProperty(e1.getInput())
                    e1_comp_string = prop

                if(isinstance(e1_comp_string, StringList)):
                    e1_comp_string = e1_comp_string.printString()
                    
                if (isinstance(e1_comp_string, int)):
                    e1_comp_string = '"' + str(e1_comp_string) + '"'
                else:
                    if(e1_comp_string != '""'):
                        e1_comp_string = '"' + e1_comp_string + '"'
                     
            if(len(e2.getPropertyList().getDict()) > 0):
                e2_comp_string = e2.getPropertyList().getProperty("string")
                if (isinstance(e2_comp_string, list)):
                    e2_comp_string = '"' + e2_comp_string[0] + '"'
                if (e2_comp_string == ""):
                    e2_comp_string = '""'
                            
            if(equals):
                if(e1_comp_string == e2_comp_string):
                    if(g.getInput() != ""):
                        return g.checkSyntax()
                    else:
                        return 1
            elif(not_equals):
                if(e1_comp_string != e2.getInput()):
                    if(g.getInput() != ""):
                        return g.checkSyntax()
                    else:
                        return 1

        return 0