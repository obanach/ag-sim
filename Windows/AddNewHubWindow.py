import customtkinter
import Entities.Hub as hub

class AddNewHubWindow(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.NewWindow = customtkinter.CTkToplevel(self.master)
        self.NewWindow.title("Właściwości Huba")
        self.NewWindow.geometry("400x200")
        self.NewWindow.resizable(False, False)
        self.NewWindow.columnconfigure(1, weight=1)

        self.LabelPairCode = customtkinter.CTkLabel(self.NewWindow, text="Kod parowania")
        self.LabelPairCode.grid(row=1, column=0, padx=(20,0), pady=20)
        self.TextBoxPairCode = customtkinter.CTkTextbox(self.NewWindow, height=25)
        self.TextBoxPairCode.grid(row=1, column=1, padx=20, pady=20, sticky='ew')

        self.SendButton = customtkinter.CTkButton(self.NewWindow, text="Zatwierdź", command=self.confirmAction)
        self.SendButton.grid(row=2, column=0, columnspan=2, padx=10, sticky='sew')
        self.NewWindow.grab_set()


    def confirmAction(self):
        data = hub.Hub(self.TextBoxPairCode.get(0.1, customtkinter.END).rstrip())
        self.master.updateHubList(data)
        self.NewWindow.destroy()