import customtkinter
import Entities.Module as mod

class NewModuleWindow(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.NewWindow = customtkinter.CTkToplevel(self.master)

        self.NewWindow.title("Właściwości modułu")
        self.NewWindow.geometry("400x200")
        self.NewWindow.resizable(False, False)
        self.NewWindow.columnconfigure(1, weight=1)

        self.LabelModuleType = customtkinter.CTkLabel(self.NewWindow, text="Typ modułu")
        self.LabelModuleType.grid(row=0, column=0, padx=(20,0), pady=20)
        self.ComboBoxModule = customtkinter.CTkComboBox(self.NewWindow, state="readonly", values=["environment", "switch"])
        self.ComboBoxModule.grid(row=0, column=1, padx=20, pady=20, sticky='ew')

        self.labelModuleName = customtkinter.CTkLabel(self.NewWindow, text="Nazwa modułu")
        self.labelModuleName.grid(row=1, column=0, padx=(20,0), pady=20)
        self.textBoxModuleName = customtkinter.CTkTextbox(self.NewWindow, height=25)
        self.textBoxModuleName.grid(row=1, column=1, padx=20, pady=20, sticky='ew')
        
        self.SendButton = customtkinter.CTkButton(self.NewWindow, text="Zatwierdź", command=self.confirmAction)
        self.SendButton.grid(row=2, column=0, columnspan=2, padx=10, sticky='sew')
        self.NewWindow.grab_set()

    def confirmAction(self):
        data = mod.Module(self.textBoxModuleName.get(0.1, customtkinter.END).rstrip(), self.ComboBoxModule.get())
        self.master.updateModuleList(data, False)
        self.NewWindow.destroy()