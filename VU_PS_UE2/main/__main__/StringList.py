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
        self.sys_return()
        self.out()
        
    def sysCall(self):
        self.property_dict.add({"syscall",self.doLinuxSysCall(self.getProperty("string"))})
        
    def IOSysCall(self):
        self.property_dict.add({"iosyscall",self.doLinuxIOSysCall(self.getProperty("string"))})
        
    def sys_return(self):
        self.property_dict.add({"return",self.doLinuxReturn(self.getProperty("string"))})
        
    def out(self):
        self.property_dict.add({"out",self.doLinuxOut(self.getProperty("string"))})
        
    def doLinuxSysCall(self,string):
        return subprocess.call(string.split(),shell=True)
    
    def doLinuxIOSysCall(self,string):
        return "" #TODO do it!!!s
    
    def doLinuxReturn(self,string):
        return "" #TODO do it!!!s
    
    def doLinuxOut(self,string):
        return "" #TODO do it!!!s