class Module():
    def __init__(self, name, type):
        self.Id = None
        self.Name = name
        self.Type = type
        self.Token = None
        self.CheckBox = None
        self.ModuleBox = None
        self.MacAddress = None
        self.Paired = False

    def __str__(self):
        return f'Id: {self.Id}, Name: {self.Name}, Type: {self.Type}'
    
    def GetProperties(self):
        return {'Id': self.Id, 'Name': self.Name, 'Type': self.Type, 'Paired': self.Paired, 'MacAddress': self.MacAddress }
    
    @staticmethod
    def CreateClass(data):
        mod = Module(data["Name"], data["Type"])
        mod.Id = data["Id"]
        mod.Paired = data["Paired"]
        mod.MacAddress = data["MacAddress"]
        return mod
