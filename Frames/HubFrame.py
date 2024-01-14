import customtkinter
import uuid

class HubFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.addModuleButton = customtkinter.CTkButton(self, text="Dodaj moduł", command=self.AddModuleCallback)
        self.addModuleButton.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.Modules = customtkinter.CTkScrollableFrame(self, width=1000)
        self.Modules.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.ModulesList = []
        self.Observers = []
    
    def addModule(self, module):
        self.ModulesList.append(module)

    def updateModuleList(self):
        i = len(self.ModulesList)
        try:
            moduleBox = customtkinter.CTkCheckBox(self.Modules, 
                                                text=str(self.ModulesList[i-1]), 
                                                command=self.deleteModuleButton)
            moduleBox.grid(row=i, column=0, sticky='w')
        except IndexError:
            print("List index out of range")
            

    def AddModuleCallback(self):
        newWindow = NewModuleWindow(self)

    def deleteModuleButton(self):
        #TODO dodac funkcje usuwania
        pass

    def Subscribe(self, observer):
        self.Observers.append(observer)

    def UnSubscribe(self, observer):
        self.Observers.remove(observer)
    
    def Notify(self, message):
        print(str(message))

class Module():
    def __init__(self, name, type):
        self.uuid = uuid.uuid4()
        self.name = name
        self.type = type
    def __str__(self):
        return f'uuid: {self.uuid}, name: {self.name}, type: {self.type}'
    def getProperties(self):
        return (self.uuid, self.name, self.type)


class NewModuleWindow(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.new_window = customtkinter.CTkToplevel(self.master)
        self.new_window.title("Właściwości modułu")
        self.new_window.geometry("400x200")
        self.new_window.minsize(400, 200)
        self.new_window.columnconfigure(1, weight=1)
        self.labelModuleType = customtkinter.CTkLabel(self.new_window, text="Typ modułu")
        self.labelModuleType.grid(row=0, column=0, padx=(20,0), pady=20)
        self.comboBoxModule = customtkinter.CTkComboBox(self.new_window, state="readonly", values=["environment", "switch"])
        self.comboBoxModule.grid(row=0, column=1, padx=20, pady=20, sticky='ew')
        self.labelModuleName = customtkinter.CTkLabel(self.new_window, text="Nazwa modułu")
        self.labelModuleName.grid(row=1, column=0, padx=(20,0), pady=20)
        self.textBoxModuleName = customtkinter.CTkTextbox(self.new_window, height=25)
        self.textBoxModuleName.grid(row=1, column=1, padx=20, pady=20, sticky='ew')
        self.sendButton = customtkinter.CTkButton(self.new_window, text="Zatwierdź", command=self.confirmAction)
        self.sendButton.grid(row=2, column=0, columnspan=2, padx=10, sticky='sew')
        self.new_window.focus()
        master.Subscribe(self)

    def confirmAction(self):
        data = Module(self.textBoxModuleName.get(0.1, customtkinter.END), self.comboBoxModule.get())
        self.master.addModule(data)
        self.master.updateModuleList()
        self.master.Notify(data)
        self.master.UnSubscribe(self)
        self.new_window.destroy()