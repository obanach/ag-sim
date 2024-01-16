import customtkinter
import Entities.Module as mod

class NewModuleWindow(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.new_window = customtkinter.CTkToplevel(self.master)

        self.new_window.title("Właściwości modułu")
        self.new_window.geometry("400x200")
        self.new_window.resizable(False, False)
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
        self.new_window.grab_set()

    def confirmAction(self):
        data = mod.Module(self.textBoxModuleName.get(0.1, customtkinter.END), self.comboBoxModule.get())
        self.master.updateModuleList(data)
        self.new_window.destroy()