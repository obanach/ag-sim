import uuid

class Hub():
    def __init__(self, pairCode):
        self.uuid = uuid.uuid4()
        self.name = None
        self.Token = None
        self.PairCode = pairCode
    def __str__(self):
        return f'uuid: {self.uuid}, name: {self.name}, token: {self.Token}'
    def getProperties(self):
        return {'Uuid': self.uuid,'Name': self.name, 'Token': self.Token}