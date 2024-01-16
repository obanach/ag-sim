import customtkinter
import asyncio
import requests
import Windows.AddNewModuleWindow as mod

#TODO
# Dodać zarządzanie hubem - dodawanie, usuwanie i odpowiednią logikę związaną z API
# Refaktor do innych klas
# Dodać usuwanie modułów
# Dodać opcję włączania/wyłączania huba
# Dodać logowanie akcji w aplikacji

class HubFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        self.addModuleButton = customtkinter.CTkButton(self, text="Dodaj moduł", command=self.AddModuleCallback)
        self.deleteModuleButton = customtkinter.CTkButton(self, text="Usuń moduł/y", fg_color = "#722b29", hover_color = "#3f1716", command=self.DeleteModuleCallback)

        self.addModuleButton.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="e")
        self.deleteModuleButton.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.master.columnconfigure(0, weight=1)

        self.Modules = customtkinter.CTkScrollableFrame(self)
        self.Modules.columnconfigure(0, weight=1)

        self.Modules.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.ModulesList = []
        self.DataFrequency = 10
        self.Id = 1

    def updateModuleList(self, modul):
        self.ModulesList.append(modul)
        self.displayModules()
        #TODO: wysłać na api rejestrowanie modułu w tym hubie
        #        https://api.autogrow.pl/device/hub/:hubId/module
      

    def AddModuleCallback(self):
        newWindow = mod.NewModuleWindow(self)
 
    def DeleteModuleCallback(self):
        modules_to_remove = []

        for module in self.ModulesList:
            if module.checkBox.get():
                modules_to_remove.append(module)

        if not modules_to_remove:
            return

        for module in modules_to_remove:
            module.moduleBox.destroy()
            self.ModulesList.remove(module)
        
        self.refreshModuleDisplay()


    def displayModules(self):
        properties = ["Uuid", "Name", "Type", "Token"]
        for i, module in enumerate(self.ModulesList):
            moduleBox = customtkinter.CTkFrame(self.Modules)
            checkBox = customtkinter.CTkCheckBox(self.Modules, text='', fg_color = "#722b29", hover_color = "#3f1716")

            module.checkBox = checkBox
            module.moduleBox = moduleBox

            moduleBox.columnconfigure(0, weight=1)
            moduleBox.grid(row=i, column=0, sticky='wens', padx=10, pady=10)
            checkBox.grid(row=i, column=1, sticky='wens', padx=10, pady=10)
            moduleData = module.getProperties()

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
                
                asyncio.sleep(self.DataFrequency)
                #TODO: dodać logikę wysyłania danych
                # 1. Sprawdzić czy hub jest włączony
                # 2. Pobrać dane z modułów
                # 3. Wysłać na endpoint
                # https://api.autogrow.pl/device/hub/:hubId/module/:moduleId/data
        except asyncio.CancelledError:
            return
    
    async def __del__(self):
        self.DataTask.cancel()