from PropertyList import PropertyList
import subprocess

class StringList(PropertyList):
    
    def __init__(self,input):
        super(StringList,self).__init__()
        self.addProperty("string", list(input))
        self.initializeSystemFunctions()

    def printString(self):
        result = ""
        for c in self.property_dict["string"]:
            result += c
        return result
    
    def initializeSystemFunctions(self):
        self.sysCall()
        self.IOSysCall()
        
    def sysCall(self):
        self.property_dict.add({"syscall",self.doLinuxSysCall(self.getProperty("string"))})
        
    def IOSysCall(self):
        self.property_dict.add({"iosyscall",self.doLinuxIOSysCall(self.getProperty("string"))})
        
    def doLinuxSysCall(self,string):
        process = subprocess.Popen(''.join(string).split(),stdout=subprocess.PIPE)
        
        fullOutput = ""
        line = process.stdout.readline()
        while line:
            line = process.stdout.readline()
            fullOutput += line
        
        process.communicate()[0]
        self.property_dict({"result",process.returncode})
        self.property_dict({"out",fullOutput})
        return process.returncode #this writes returncode to "syscall" as well
    
    def doLinuxIOSysCall(self,string):
        process = subprocess.Popen(''.join(string).split(),stdout=subprocess.PIPE)
        
        fullOutput = ""
        line = process.stdout.readline()
        while line:
            line = process.stdout.readline()
            fullOutput += line
        
        self.property_dict({"out",fullOutput})
        return fullOutput#TODO what goes here, IOSysCall should be a property in list, right?