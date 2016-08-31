from PropertyList import PropertyList
import subprocess
#import sys

class StringList(PropertyList, object):
    
    def __init__(self,input):
        super(StringList,self).__init__()
        self.addProperty("string", list(input))
        #self.initializeSystemFunctions()

    def printString(self):
        result = ""
        if(isinstance(self.property_dict["string"], int)):
            result = str(self.property_dict["string"])
#             if(result[0] == "'" & result[-1] == "'"):
#                 result = result[1:-1]
        else:
            for c in self.property_dict["string"]:
                result += c
        return result
    
    #printing everything and just returning one value
    def doLinuxSysCall(self,string):
        process = subprocess.Popen(''.join(string).split(),stdout=subprocess.PIPE)
        
        line = process.stdout.readline()
        while line:
            if len(line) is not 0:
                print line.rstrip('\n')
            line = process.stdout.readline()
            
        if len(line) is not 0:
            print line.rstrip('\n')
        
        process.communicate()[0]
        return process.returncode #this writes return code to "syscall"
    
    #"out", "err" and "result" saved in new property list, print output?
    def doLinuxIOSysCall(self, string, in_string):
        IOSysCallList = PropertyList()
        if(string.startswith("echo")):
            string += ' ' + in_string;
            in_string = ""
        process = subprocess.Popen(''.join(string).split(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if(in_string != ""):
            fullOutput, fullError = process.communicate(in_string + ' \n')
        else:
            fullOutput, fullError = process.communicate()
        
        if(fullOutput[-1] == '\n'):
            fullOutput = fullOutput[:-1]
            
        print fullOutput                 
        IOSysCallList.addProperty("out",fullOutput)
        IOSysCallList.addProperty("err",fullError)
        IOSysCallList.addProperty("result",process.returncode)
        return IOSysCallList
    
    #the prompt saves its answer
    def promptUserInput(self,string):
        userinput = raw_input(''.join(string)) #TODO check if string has newline
        #print "Your input " + input + " was saved."
        inputList = StringList(userinput)
        return inputList
    
    #directly filled as a property of the string, called as ".length"
    def stringLength(self):
        self.property_dict.update({"length",len(self.getProperty("string"))})
    
    #removing leading and trailing spaces, newlines and tabs, called as ".trim"
    def trim(self):
        trimmed = ''.join(self.getProperty("string")).strip()
        self.property_dict.update({"trim",trimmed})
        
    #checks whether string is numeric, writes 0 or 1 into "isnumeric", called as ".isnumeric"
    def isnumeric(self):
        isnumeric = 0
        string = ''.join(self.getProperty("string"))
        if string.isdigit():
            isnumeric = 1
        elif (string[0] == '-') and string[1:].isdigit():
            isnumeric = 1
        self.property_dict.update({"isnumeric",isnumeric})