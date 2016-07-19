from PropertyList import PropertyList

class StringList(PropertyList):
    
    def __init__(self,input):
        super(StringList,self).__init__()
        self.addProperty("string", list(input))

    def printString(self):
        result = ""
        for c in self.property_dict["string"]:
            result += c
        return result