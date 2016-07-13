from PropertyList import PropertyList

class StringList(PropertyList):
    
    def __init__(self,input):
        super(StringList,self).__init__()
        self.addProperty(input, list(input))
