import customtkinter
import asyncio
import Windows.AddNewModuleWindow as mod
import requests
import Entities.GlobalVariables as gv
import json
import aiohttp
import Services.MqttClient as mqtt
import Entities.Module as emod
import Entities.Hub as ehub

class HubFrame(customtkinter.CTkFrame):
    def __init__(self, master, asyncioLoop, hubData, modules = None):
        super().__init__(master)
        self.HubData = hubData
        self.MqttClient = mqtt.MQTTClient(self, self.HubData.MqttUsername, self.HubData.MqttPassword, self.HubData.Id)
        self.MqttClient.connect("mqtt.autogrow.pl")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        self.AddModuleButton = customtkinter.CTkButton(self, text="Dodaj moduł", command=self.AddModuleCallback)

        self.AddModuleButton.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")
        self.master.columnconfigure(0, weight=1)

        self.Modules = customtkinter.CTkScrollableFrame(self)
        self.Modules.columnconfigure(0, weight=1)

        self.Modules.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.ModulesList = []
        if modules is not None:
            for a in modules:
                self.ModulesList.append(a)
        
        self.AsyncioLoop = asyncioLoop
        self.displayModules()
        self.DataTask = asyncio.run_coroutine_threadsafe(self.SendData(), self.AsyncioLoop)


    def GetProperties(self):
        return {'HubName': self.HubData.Name, 'HubData': self.HubData.GetProperties(), 'ModulesList': [obj.GetProperties() for obj in self.ModulesList]}
    
    @staticmethod
    def CreateClass(master,loop,data):
        hubName = data["HubName"]
        modules = [emod.Module.CreateClass(obj) for obj in data["ModulesList"]]
        hubData = ehub.Hub.CreateClass(data["HubData"])
        return HubFrame(master,loop, hubData,modules)

    def updateModuleList(self, modul, refresh=False):
        if not refresh:
            modul.MacAddress = gv.GlobalVariables.GenerateRandomMacAddress()
            self.ModulesList.append(modul)
        else:
            modu = None
            for mod in self.ModulesList:
                if mod.MacAddress == modul.MacAddress:
                    modu=mod
                    break
            baseUrl = gv.GlobalVariables.AddNewModule()
            fullUrl = baseUrl.format(self.HubData.Id)
            data = {"type": modu.Type, "name": modu.Name, "macAddress": modu.MacAddress}
            headers = {"X-Device-Token": self.HubData.Token, "Content-Type": "application/json"}
            response = requests.post(url=fullUrl, 
                                 data=json.dumps(data),
                                   headers=headers)
            data = response.json()
            modul.Id = data["id"]
            # w tym przypadku otrzymujemy false modul wktórym jest id, MacAddress 
            # szukamy tego modułu, ustawiamy Id oraz zmieniamy status na sparowany
            for mod in self.ModulesList:
                if mod.MacAddress == modul.MacAddress:
                    mod.Id = modul.Id
                    mod.Name = modul.Name
                    mod.Paired = True
                    break
            
            self.MqttClient.publish(
                f"hub/{self.HubData.Id}/module/pair", 
                json.dumps({
                    "header": {"type": "response"},
                    "body": {
                        "paired": True, 
                        "macAddress": modul.MacAddress, 
                        "id": modul.Id
                    }
                })
            )

        self.displayModules()
      

    def AddModuleCallback(self):
        newWindow = mod.NewModuleWindow(self)
 
    def DeleteModuleCallback(self, macAddress):
        toRemove = None
        for module in self.ModulesList:
            if module.MacAddress == macAddress:
                toRemove = module
                break

        if toRemove == None:
            return
        toRemove.ModuleBox.destroy()
        self.ModulesList.remove(toRemove)
        baseUrl = gv.GlobalVariables.DeleteModuleFromHub()
        fullUrl = baseUrl.format(self.HubData.Id, toRemove.Id)
        headers = {"X-Device-Token": self.HubData.Token, "Content-Type": "application/json"}
        response = requests.delete(url=fullUrl,
                                  headers=headers)
        self.MqttClient.publish(
            f"hub/{self.HubData.Id}/module/delete", 
            json.dumps({
                "header": {"type": "response"},
                "body": {
                    "paired": False, 
                    "id": toRemove.Id
                }
            })
        )
        # jest ale pomijamy co odpowiedział serwer
        self.refreshModuleDisplay()


    def DeleteModuleById(self, moduleId):
        toRemove = None
        for module in self.ModulesList:
            if module.Id == moduleId:
                toRemove = module
                break

        if toRemove == None:
            return
        toRemove.ModuleBox.destroy()
        self.ModulesList.remove(toRemove)
        baseUrl = gv.GlobalVariables.DeleteModuleFromHub()
        fullUrl = baseUrl.format(self.HubData.Id, toRemove.Id)
        headers = {"X-Device-Token": self.HubData.Token, "Content-Type": "application/json"}
        response = requests.delete(url=fullUrl,
                                  headers=headers)
        # jest ale pomijamy co odpowiedział serwer
        self.MqttClient.publish(
            f"hub/{self.HubData.Id}/module/delete", 
            json.dumps({
                "header": {"type": "response"},
                "body": {
                    "paired": False, 
                    "id": toRemove.Id
                }
            })
        )
        
        self.refreshModuleDisplay()

    def displayModules(self):
        properties = ["Id", "Name", "Type", "Paired"]
        for i, module in enumerate(self.ModulesList):
            moduleBox = customtkinter.CTkFrame(self.Modules)
            deleteModuleButton = customtkinter.CTkButton(self.Modules, text="Usuń moduł",
                                                          fg_color = "#722b29", hover_color = "#3f1716",
                                                            command=lambda macAddress=module.MacAddress: self.DeleteModuleCallback(macAddress))

            module.CheckBox = deleteModuleButton
            module.ModuleBox = moduleBox

            moduleBox.columnconfigure(0, weight=1)
            moduleBox.grid(row=i, column=0, sticky='wens', padx=10, pady=10)
            deleteModuleButton.grid(row=i, column=1, sticky='wens', padx=10, pady=10)
            moduleData = module.GetProperties()

            for j, property in enumerate(properties):
                label = customtkinter.CTkLabel(moduleBox, text=f"{property}: {moduleData[property]}")
                label.grid(row=j, column=0, sticky='we')


    def refreshModuleDisplay(self):
        for widget in self.Modules.winfo_children():
            widget.destroy()

        self.displayModules()


    async def SendData(self):
        try:
            while True:
                print(self.HubData.DataFrequency)
                await asyncio.sleep(self.HubData.DataFrequency)
                moduleData = []
                moduleIds = []
                for moduleUnit in self.ModulesList:
                    if moduleUnit.Type == "environment" and moduleUnit.Id:
                        print(moduleUnit)
                        moduleData.append(gv.GlobalVariables.GetEnvironmentData())
                        moduleIds.append(moduleUnit.Id)
                for data, moduleId in zip(moduleData, moduleIds):
                    async with aiohttp.ClientSession() as session:
                        baseUrl = gv.GlobalVariables.PostModuleData()
                        fullUrl = baseUrl.format(self.HubData.Id, moduleId)
                        print(fullUrl)
                        headers = {"X-Device-Token": self.HubData.Token, "Content-Type": "application/json"}
                        async with session.post(fullUrl, headers = headers, json=data) as response:
                            response_data = await response.text()
                            serializedData = json.loads(response_data)
                            if 'message' in serializedData:
                                if serializedData["message"] == "Hub not found":
                                    #TODO wywalić wtedy tego huba
                                    pass
                                if serializedData["message"] == "TODO":
                                    #sprawdzić co otrzymuje jako response przy próbie wysłania danych gdy usunieto moduł z poziomu strony
                                    pass
                            #print(f"{moduleId}: {response_data}")
        except Exception as err:
            print(err)
            return
        
    async def HeartBeat(self):
        for module in self.ModulesList:
            async with aiohttp.ClientSession() as session:
                baseUrl = gv.GlobalVariables.GetHeartBeatEndpoint()
                fullUrl = baseUrl.format(self.HubData.Id, module.Id)
                headers = {"X-Device-Token": self.HubData.Token, "Content-Type": "application/json"}
                async with session.post(fullUrl, headers = headers) as response:
                    response_data = await response.text()
                    #print(f"{module.Id}: {response_data}")
        async with aiohttp.ClientSession() as session:
            baseUrl = gv.GlobalVariables.HubHeartbeatEndpoint()
            fullUrl = baseUrl.format(self.HubData.Id)
            headers = {"X-Device-Token": self.HubData.Token, "Content-Type": "application/json"}
            async with session.post(fullUrl, headers = headers) as response:
                response_data = await response.text()
                #print(f"{self.HubData.Id}: {response_data}")

    def GetUnpairedModules(self):
        unpaired = []
        for mod in self.ModulesList:
            if mod.Paired == False:
                unpaired.append(mod)
        unpairedParsed =[]
        for mod in unpaired:
            module_json = {
                "name": mod.Name,
                "type": mod.Type,
                "macAddress": mod.MacAddress  # Assuming MacAddress is set correctly in your Module class
            }
            unpairedParsed.append(module_json)
        
        response_json = {
            "header": {"type": "response"},
            "body": {"modules": unpairedParsed}
        }

        return json.dumps(response_json, indent=4)  # Serializes the dictionary to a JSON formatted string
    
    def GetPairedModules(self):
        paired = []


    def __del__(self):
        self.DataTask.cancel()

    
