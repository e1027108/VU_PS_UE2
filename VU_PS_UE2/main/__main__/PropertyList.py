class PropertyList:
    
    def __init__(self):
        self.property_dict = {}
    
    def addProperty(self,name,value):
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