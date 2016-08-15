
class PropertyList:
    
    def __init__(self):
        self.property_dict = {}
    
    def addProperty(self,name,value):
        if isinstance(value,basestring):
            if (not (value.startswith('"') and value.endswith('"'))):
                self.property_dict.update({name:value})
            else:
                from StringList import StringList
                if(len(value) == 2):
                    self.property_dict.update({name:""})
                else:
                    self.property_dict.update({name:StringList(value[1:-1])})
        else:
            self.property_dict.update({name:value})
    
    def changeProperty(self,name,newValue):
        if self.exists(name):
            self.addProperty(name,newValue)
        else:
            raise KeyError #means code in our language is faulty
    
    def deleteProperty(self,name):
        del self.property_dict[name]        
    
    def getProperty(self,name):
        return self.property_dict[name]
    
    def exists(self,name):
        return (name in self.property_dict)
    
    def getDict(self):
        return self.property_dict
    
    def printList(self):
        from StringList import StringList
        print "Entries in the property list (name: value):"
        for key in self.property_dict:
            value = self.property_dict[key]
            if isinstance(value, basestring):
                print key + ": " + value
            elif isinstance(value,StringList):
                print key + ": " + value.printString()
            elif isinstance(value, list):
                result = key + ": "
                for c in value:
                    result += c
                print result