import customtkinter
import Entities.Hub as hub

class AddNewHubWindow(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.new_window = customtkinter.CTkToplevel(self.master)
        self.new_window.title("Właściwości Huba")
        self.new_window.geometry("400x200")
        self.new_window.resizable(False, False)
        self.new_window.columnconfigure(1, weight=1)

        self.LabelPairCode = customtkinter.CTkLabel(self.new_window, text="Kod parowania")
        self.LabelPairCode.grid(row=1, column=0, padx=(20,0), pady=20)
        self.TextBoxPairCode = customtkinter.CTkTextbox(self.new_window, height=25)
        self.TextBoxPairCode.grid(row=1, column=1, padx=20, pady=20, sticky='ew')

        self.sendButton = customtkinter.CTkButton(self.new_window, text="Zatwierdź", command=self.confirmAction)
        self.sendButton.grid(row=2, column=0, columnspan=2, padx=10, sticky='sew')
        self.new_window.grab_set()


    def confirmAction(self):
        data = hub.Hub(self.TextBoxPairCode.get(0.1, customtkinter.END))
        self.master.updateHubList(data)
        self.new_window.destroy()