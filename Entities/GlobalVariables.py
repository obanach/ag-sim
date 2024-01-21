import random
import math
import random

class GlobalVariables:
    @staticmethod
    def PairHubEndpoint():
        return "https://api.autogrow.pl/device/hub/pair"
    @staticmethod
    def GetEnvironmentData():
        temperature = random.randint(18, 23)
        humidity = random.randint(30, 40) + 75
        dirt = random.randint(30, 33) + 46
        battery = random.randint(30, 33) + 46

        data = {
            "temperature": temperature,
            "humidity": humidity,
            "dirt": dirt,
            "battery": battery
        }
        return data
    @staticmethod
    def AddNewModule():
        return "https://api.autogrow.pl/device/hub/{}/module"
    @staticmethod
    def GenerateRandomMacAddress():
        return "%02x:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255))
    @staticmethod
    def DeleteHubEndpoint():
        return "https://api.autogrow.pl/device/hub/{}"
    @staticmethod
    def DeleteModuleFromHub():
        return "https://api.autogrow.pl/device/hub/{}/module/{}"
    @staticmethod
    def PostModuleData():
        return "https://api.autogrow.pl/device/hub/{}/module/{}/data"
    @staticmethod
    def GetHeartBeatEndpoint():
        return "https://api.autogrow.pl/device/hub/{}/module/{}/ping"
    def HubHeartbeatEndpoint():
        return "https://api.autogrow.pl/device/hub/{}/ping"