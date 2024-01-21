import customtkinter
import Frames.HubFrame as Frames
import Windows.AddNewHubWindow as hub
import Entities.GlobalVariables as gv
import requests
import Services.MqttClient as mqtt
import json
import asyncio

class App(customtkinter.CTk):
    def __init__(self, asyncioLoop):
        super().__init__()
        self.title("Hub Simulator")
        self.minsize(640,480)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.TabView = customtkinter.CTkTabview(self, anchor='nw')
        self.CreateHubButton = customtkinter.CTkButton(self, text="Dodaj Huba", command=self.AddNewHubCallback)
        self.DeleteHubButton = customtkinter.CTkButton(self, fg_color = "#722b29", hover_color = "#3f1716", text="Usuń Huba", command=self.DeleteHubCallback)
        self.CreateHubButton.grid(column=1, row=0, sticky='wesn')
        self.DeleteHubButton.grid(column=0, row=0, sticky='wesn')
        self.TabView.grid(column=0, columnspan=2, row=1, sticky='wesn')
        self.FrequencyButton = customtkinter.CTkButton(self, text="Zmień delay", command=self.FrequencyRateDialog)
        self.FrequencyButton.grid(row=2, column=1, sticky='e', pady=10, padx=10)

        self.AsyncioLoop = asyncioLoop
        self.HubList = []
        self.deserialize("hubs.txt")
        self.HeartBeatTask = asyncio.run_coroutine_threadsafe(self.SendHeartBeat(), self.AsyncioLoop)

    def FrequencyRateDialog(self):
        hubCheck = self.TabView.get()
        if not hubCheck:
            return
        inputDialog = customtkinter.CTkInputDialog(text="Zmień delay")
        frequency = inputDialog.get_input()
        for hub in self.HubList:
            if hubCheck == hub.HubData.Name:
                hub.HubData.DataFrequency = int(frequency)

    def deserialize(self,filename, class_=Frames.HubFrame):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                if isinstance(data, list):
                    for item in data:
                        self.TabView.add(f"{item['HubName']}")
                        newClass = class_.CreateClass(self.TabView.tab(f"{item['HubName']}"),self.AsyncioLoop,item)
                        newClass.pack(expand=True, fill='both')
                        self.HubList.append(newClass)
                else:
                    print("Incorrect data format")
        except (FileNotFoundError):
            print("File was not found")
        except(json.JSONDecodeError):
            print("Incorrect file format")


    def AddNewHubCallback(self):
        hub.AddNewHubWindow(self)

    def DeleteHubCallback(self):
        hubToDeleteName = self.TabView.get()
        if not hubToDeleteName:
            return
        
        self.TabView.delete(hubToDeleteName)
        
        toDeleteFromHubList = None
        for hub in self.HubList:
            if hub.HubData.Name == hubToDeleteName:
                toDeleteFromHubList = hub
                self.HubList.remove(toDeleteFromHubList)

        baseUrl = gv.GlobalVariables.DeleteHubEndpoint()
        fullUrl = baseUrl.format(toDeleteFromHubList.HubData.Id)
        headers = {"X-Device-Token": hub.HubData.Token, "Content-Type": "application/json"}
        response = requests.delete(url=fullUrl, headers=headers)
        data = response.json()
        #wynik operacji otrzymujemy i nic z tym nie robimy


    def updateHubList(self, hub):
        data = {'pairCode': hub.PairCode}
        response = requests.post(url=gv.GlobalVariables.PairHubEndpoint(), data=json.dumps(data))
        data = response.json()

        message = data.get('message')
        if message is not None:
            return

        hub.Name = data['name']
        hub.Id = data['id']
        hub.Token = data['accessToken']
        hub.MqttData = data['mqtt']
        hub.MqttUsername = hub.MqttData["username"]
        hub.MqttPassword = hub.MqttData["password"]

        self.TabView.add(f"{data['name']}")
        Hub = Frames.HubFrame(self.TabView.tab(f"{data['name']}"),self.AsyncioLoop, hub)

        Hub.pack(expand=True, fill='both')
        self.HubList.append(Hub)

    def serialize(self,obj):
        if isinstance(obj, list):
            return [self.serialize(item) for item in obj]
        elif hasattr(obj, "GetProperties"):
            return obj.GetProperties()

    def SaveHubs(self):
        with open("hubs.txt", "w") as file:
            json.dump(self.HubList, file, default=self.serialize, indent=4)

    async def SendHeartBeat(self):
        try:
            while True:
                await asyncio.sleep(60)
                for hub in self.HubList:
                    await hub.HeartBeat()
        except Exception as err:
            print(err)
            return

    def __del__(self):
        self.HeartBeatTask.cancel()

