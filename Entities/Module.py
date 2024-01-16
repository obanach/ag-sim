import uuid

class Module():
    def __init__(self, name, type):
        self.uuid = uuid.uuid4()
        self.name = name
        self.type = type
        self.Token = None
        self.checkBox = None
        self.moduleBox = None

    def __str__(self):
        return f'uuid: {self.uuid}, name: {self.name}, type: {self.type}, token: {self.Token}'

    def getProperties(self):
        return {'Uuid': self.uuid, 'Name': self.name, 'Type': self.type, 'Token': self.Token}
