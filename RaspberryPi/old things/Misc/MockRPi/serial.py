class Serial:
    
    def __init__(self,string1, number):
        self.string = string1
        self.number = number
        self.count = 0
        
    def write(self, string1):
        self.count = self.count + 1
        
    def getCount(self):
        print(self.count)