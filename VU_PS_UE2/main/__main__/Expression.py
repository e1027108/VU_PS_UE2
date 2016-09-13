'''
Created on 21. Juni 2016

@author: raidsnail
'''
from Component import Component
import sys

class Expression(Component):
    
    def __init__(self,input,parent):
        self.previous = None
        self.exec_list = {"syscall", "iosyscall", "userinput", "length", "trim", "isnumeric", "print"}
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
        
        names_array = None
        
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
                        names_array = [part2]
                    if " " in part2:
                        spaceIndex = part2.find(" ")
                        print ("There is a ';' missing at Index " + str(len(part1) + spaceIndex) + " in the name part of Expression:"  + test)
                        return False
                    if "." in part2:
                        names_array = part2.split(".")
                        for n in names_array:
                            if (len(n) > 1 and n[1].isalpha() and names):
                                names = self.checkName(n)
                        if (not names):
                            print("There is a misplaced '.' in the name variable. This is an invalid Expression: " + test)
                            return False 
                            
                        part2 = names_array[0]   
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
            if(self.checkPart1(part1) and names):
                if(self.syntax_only == False):
                    if(names_array != None):
                        for n in names_array:
                            if (n in self.exec_list):
                                self.handleLinuxCommand(n)
                            else:
                                if '"' in part1:
                                    from StringList import StringList
                                    self.property_list = StringList(str(self.property_list.getProperty(n)))
                                else:
                                    from StringList import StringList
                                    self.property_list = StringList(str(self.property_list.getProperty(part1.lstrip('*') + "." + n)))
                        
                    if(self.previous != None):
                        stars = self.countStartOccurrences(part1,'*')
                        self.property_list = self.concatenate(self.previous, self.property_list, stars)
                        
                                         
                return True                    
        else:
            if(self.checkPart1(part1)):
                if(self.syntax_only == False):
                    if(names_array != None):
                        for n in names_array:
                            if (n in self.exec_list):
                                self.handleLinuxCommand(n)
                            else:
                                if '"' in part1:
                                    from StringList import StringList
                                    self.property_list = StringList(str(self.property_list.getProperty(n)))
                                else:
                                    from StringList import StringList
                                    self.property_list = StringList(str(self.property_list.getProperty(part1.lstrip('*') + "." + n)))
                                
                    if(self.previous != None):
                        stars = self.countStartOccurrences(part1,'*')                        
                        self.property_list = self.concatenate(self.previous, self.property_list, stars)
            
                
                    e.previous = self.property_list
                if (names and e.checkSyntax()):
                    if(self.syntax_only == False):
                        if (part2 in self.exec_list):
                            self.handleLinuxCommand(part2)
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
                parent = self.escapeNestings(parent,nameIndex)
                
                #print "name: " + name
                #parent.getPropertyList().printList()
                    
               
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
                self.property_list.stringLength()
            if(part2 == "trim"):
                self.property_list.trim()
            if(part2 == "isnumeric"):
                self.property_list.isnumeric()
            if(part2 == "print"):
                self.property_list.handlePrintCommand()