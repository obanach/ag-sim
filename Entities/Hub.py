class Hub():
    def __init__(self, pairCode):
        self.Id = None
        self.Name = None
        self.Token = None
        self.PairCode = pairCode
        self.MqttClient = None
        self.MqttUsername = None
        self.MqttPassword = None
        self.DataFrequency = 5

    def __str__(self):
        return f'Id: {self.Id}, Name: {self.Name}, Token: {self.Token}'
    
    def GetProperties(self):
        return {'Id': self.Id, 'Name': self.Name, 'Token': self.Token, 'PairCode': self.PairCode, 'MqttUsername': self.MqttUsername, 'MqttPassword': self.MqttPassword}
    
    @staticmethod
    def CreateClass(data):
        hub = Hub(data["PairCode"])
        hub.Id = data["Id"]
        hub.Name = data["Name"]
        hub.Token = data["Token"]
        hub.MqttUsername = data["MqttUsername"]
        hub.MqttPassword = data["MqttPassword"]
        return hub