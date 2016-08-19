from PropertyList import PropertyList
import subprocess
import sys

class StringList(PropertyList, object):
    
    def __init__(self,input):
        super(StringList,self).__init__()
        self.addProperty("string", list(input))
        #self.initializeSystemFunctions()

    def printString(self):
        result = ""
        for c in self.property_dict["string"]:
            result += c
        return result
    
    #def initializeSystemFunctions(self):
    #    self.sysCall()
    #    self.IOSysCall()
        
    def sysCall(self):
        self.property_dict.update({"syscall",self.doLinuxSysCall(self.getProperty("string"))})
        
    def IOSysCall(self):
        self.property_dict.update({"iosyscall",self.doLinuxIOSysCall(self.getProperty("string"))})
        
    #There is supposed to be a prompt in the file, for which an input is gathered
    def userInput(self):
        self.property_dict.update({"userinput",self.promptUserInput("string")})
        
    #printing everything and just returning one value
    def doLinuxSysCall(self,string):
        process = subprocess.Popen(''.join(string).split(),stdout=subprocess.PIPE)
        
        line = process.stdout.readline()
        while line:
            print line.rstrip('\n')
            line = process.stdout.readline()
            
        print line.rstrip('\n')
        
        process.communicate()[0]
        return process.returncode #this writes return code to "syscall"
    
    #"out", "err" and "result" saved in new property list, print output?
    def doLinuxIOSysCall(self,string):
        IOSysCallList = PropertyList()
        process = subprocess.Popen(''.join(string).split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        fullOutput = ""
        fullError = ""
        
        line = process.stdout.readline()
        fullOutput += line
        while line:
            line = process.stdout.readline()
            fullOutput += line
            
        line = process.stderr.readline()
        fullError += line
        while line:
            line = process.stderr.readline()
            fullError += line
        
        IOSysCallList.addProperty("out",fullOutput)
        IOSysCallList.addProperty("err",fullError)
        process.communicate()[0]
        IOSysCallList.addProperty("result",process.returncode)
        return IOSysCallList
    
    #TODO useful?
    def promptUserInput(self,string):
        input = raw_input(string)
        #print "Your input " + input + " was saved."
        inputList = StringList(input)
        return inputList