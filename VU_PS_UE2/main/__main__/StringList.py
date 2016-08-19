from PropertyList import PropertyList
import subprocess

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
        
    #printing everything and just returning one value
    def doLinuxSysCall(self,string):
        process = subprocess.Popen(''.join(string).split(),stdout=subprocess.PIPE)
        
        line = process.stdout.readline()
        while line:
            print line
            line = process.stdout.readline()
            
        print line
        
        process.communicate()[0]
        return process.returncode #this writes returncode to "syscall"
    
    #"out" and "result" saved in new propertylist, print output?
    def doLinuxIOSysCall(self,string):
        IOSysCallList = PropertyList()
        process = subprocess.Popen(''.join(string).split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        fullOutput = ""
        
        line = process.stdout.readline()
        while line:
            line = process.stdout.readline()
            fullOutput += line
        
        IOSysCallList.addProperty("out",fullOutput)
        process.communicate()[0]
        IOSysCallList.addProperty("result",process.returncode)
        return IOSysCallList