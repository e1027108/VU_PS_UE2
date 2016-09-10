'''
Created on 21. Juni 2016

@author: raidsnail
'''
from Component import Component
import sys

class Expression(Component):
    
    def __init__(self,input,parent):
        self.previous = None
        self.exec_list = {"syscall", "iosyscall", "userinput", "length", "trim", "isnumeric"}
        super(Expression,self).__init__(input,parent)
        
    def setPrevious(self, prop_list):
        self.previous = prop_list        

    def checkSyntax(self):
        
        test = self.input.lstrip()
        test = test.rstrip()
        
        nameIndex = 0
        expIndex = 0
        
        stringOpen = False
        blockOpen = False
        expOpen = False 
        
        blockOpenCounter = 0
        blockCloseCounter = 0
        
        expOpenCounter = 0
        expCloseCounter = 0
        
        names = True
        
        part1 = test
        
        part2 = None
        
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
                if (test[x] == '.'):
                    # this is a name starting with .
                    if (nameIndex == 0):
                        part1 = test[nameIndex:x]
                    part2 = test[x+1:]
                    if " " in part2:
                        spaceIndex = part2.find(" ")
                        print ("There is a ';' missing at Index " + str(len(part1) + spaceIndex) + " in the name part of Expression:"  + test)
                        return False
                    if "." in part2:
                        dotIndex = part2.find(".")
                        if(len(part2) < dotIndex+1):
                            if (part2[dotIndex+1].isalpha()):
                                part2 = part2[:dotIndex]  
                        else:
                            print("There is a misplaced '.' in the name variable. This is an invalid Expression: " + test)
                            return False                          
                    names = self.checkName(part2)
                    nameIndex = x+1
                elif(test[x] == '+' and expIndex == 0):
                    # optional expression
                    e = Expression(test[x+1:],self.getParent())
                    e.setSyntaxOnly(self.syntax_only)
                    if(nameIndex == 0):
                        part1 = test[:x-1]
                    expIndex = x+1
                    break       
                
        # A + B + C -> write A + B in B property list if A (previous) exists 
        #if(self.previous != None):
        #    self.property_list = self.concatenate(self.previous, self.property_list)
        
        if (expIndex == 0):
            #return (self.checkPart1(part1) and names)
            if(not(part2 in self.exec_list) and part2 != None):
                part1 = test
            if(self.checkPart1(part1) and names):
                if(self.syntax_only == False):
                    if (part2 in self.exec_list):
                        self.handleLinuxCommand(part2)
                    
                        
                    if(self.previous != None):
                        stars = self.countStartOccurrences(part1,'*')
                        #print part1 + ", stars: " + str(stars) + " (1)"
                        self.property_list = self.concatenate(self.previous, self.property_list, stars)
                        
                                         
                return True                    
        else:
            #return (self.checkPart1(part1) and names and e.checkSyntax())
            if(self.checkPart1(part1)):
                if(self.syntax_only == False):
                    if (part2 in self.exec_list):
                            self.handleLinuxCommand(part2)
                    if(self.previous != None):
                        stars = self.countStartOccurrences(part1,'*')
                        #print part1 + ", stars: " + str(stars) + " (2)"
                        self.property_list = self.concatenate(self.previous, self.property_list, stars)
            
                
                    e.previous = self.property_list
                if (names and e.checkSyntax()):
                    if(self.syntax_only == False):
                        if (part2 in self.exec_list):
                            self.handleLinuxCommand(part2)
                        #self.property_list = self.concatenate(self.property_list, e.getPropertyList())
                        #self.property_list = self.concatenate(self.property_list, e.getPropertyList())
                        self.property_list = e.getPropertyList()
                        
                    return True                
                
        return False               

        
    def checkPart1(self, test):
        
        if (test[0] == '"' and test[len(test)-1] == '"'):
            # this is a string literal
            return self.checkStringLiteral(test)
        elif (test[0] == '{' and test[len(test)-1] == '}'):
            # this is a block
            from Block import Block
            #print test[0:len(test)]
            b = Block(test[0:len(test)],self.getParent())
            b.setSyntaxOnly(self.syntax_only)
            if (b.checkSyntax()):
                if(self.syntax_only == False):
                    self.property_list = b.property_list
                return True
            else:
                return False       
        elif (test[0] == '(' and test[len(test)-1] == ')'):
            # this is an expression
            e = Expression(test[1:len(test)-1],self.getParent())
            e.setSyntaxOnly(self.syntax_only)
            if (e.checkSyntax()):
                if(self.syntax_only == False):
                    self.property_list = e.property_list
                return True
            else:
                return False
        elif not (self.checkAsterisk(test)):
            # this is a name with none or multiple *
            print ("This is an invalid Expression: " + test)
            return False
        return True
    
    def checkStringLiteral(self, test):
        
        test = test[1:len(test)-1]
        k = '"'
    
        if k in test:
            print ("String literals must not contain a '\"'. This is an invalid string literal: " + test)
            return False
        
        if len(test) < 1:
            return True
        
        if(self.syntax_only == False):
            test = '"' + test + '"'
            ########self.property_list.addProperty("stringliteral", test)
            from StringList import StringList
            self.property_list = StringList(test[1:-1])
        return True
    
    def checkAsterisk(self, part):
        test = part.lstrip()
        test = test.rstrip()
        
        nameIndex = 0
        otherIndex = len(test)
                
        for x in range(0, len(test)):
            if (test[x] == '*'):
                nameIndex +=1
            elif ((test[x] == '.' or test[x] == '+') and otherIndex == len(test)):
                otherIndex = x-1
                break
            
        
        if(otherIndex != len(test)):              
            if not (self.checkName(test[nameIndex:otherIndex])):
                return False
        elif not(self.checkName(test[nameIndex:])):
            return False
        
        if(self.syntax_only == False):
        
            name = test[nameIndex:]
#
            parent = self.getParent() 
            if(nameIndex > -1):
  
                #print name + ", ind: " + str(nameIndex) + ", nest: " + str(self.getNested())
                
                # get referred parent block
                for i in range(0, nameIndex):
                    if parent.getNested() > 0:
                        for j in range(0,parent.getNested()):
                            parent = parent.getParent()
                    parent = parent.getParent()
                
                #print "name: " + name
                #parent.getPropertyList().printList()
                    
                name_helper = name.split(".")
                
                if (len(name_helper) > 1):
                    for i in range(0, len(name_helper)-1):
                        if(parent.property_list.exists(name_helper[i])):
                            prop = parent.property_list.getProperty(name_helper[i])
                           
                            from PropertyList import PropertyList
                                
                            if(isinstance(prop, PropertyList)):
                                parent = prop
                            else:
                                return False
                            
                    if(parent.exists(name_helper[len(name_helper)-1])):
                        #self.property_list.addProperty(name, parent.getProperty(name_helper[len(name_helper)-1]))
                        #self.property_list.addProperty("string", parent.getProperty(name_helper[len(name_helper)-1]))
                        from StringList import StringList
                        self.property_list = StringList(str(parent.getProperty(name_helper[len(name_helper)-1])))
                        return True
                    else:
                        return False
                
                else:
                    if(parent.property_list.exists(name)):
                        from StringList import StringList
                        if(isinstance(parent.getPropertyList().getProperty(name),StringList)):
                            self.property_list = StringList(parent.getPropertyList().getProperty(name).printString())
                        else:
                            self.property_list.addProperty(name,parent.getPropertyList().getProperty(name))
                        return True
                    else:
                        self.property_list.addProperty(name,"")
                        return True
        return True
                        
           
    def handleLinuxCommand(self, part2):
        from StringList import StringList
        if(isinstance(self.property_list, StringList)):
            if(part2 == "syscall"):
                returnCode = self.property_list.doLinuxSysCall(self.property_list.printString())
                self.property_list.changeProperty("string", returnCode)
            if(part2 == "iosyscall"):
                if(self.property_list.printString() == ""):
                    print("Cannot execute iosyscall on empty string!")
                    sys.exit()
                if(self.previous == None):
                    print("Cannot execute iosyscall for '" + self.property_list.printString() + 
                          "'\nThere is a block with an inputstream missing!")
                    sys.exit()
                if not(self.previous.exists("in")):
                    print("Cannot execute iosyscall for '" + self.property_list.printString() +
                          "'\nThere is an inputstream missing in the previous block section!")
                    sys.exit()
                syscallList = self.property_list.doLinuxIOSysCall(self.property_list.printString(),self.previous.getProperty("in").printString())
                self.property_list = syscallList
            if(part2 == "userinput"):
                inputList = self.property_list.promptUserInput(self.property_list.printString())
                self.property_list = inputList
            if(part2 == "length"):
                self.property_list.stringLength(self.property_list.printString())
            if(part2 == "trim"):
                self.property_list.trim(self.property_list.printString())
            if(part2 == "isnumeric"):
                self.property_list.isnumeric(self.property_list.printString())
                