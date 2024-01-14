import customtkinter
import Frames.HubFrame as Frames

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.HubFrame = Frames.HubFrame(self)
        self.HubFrame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")


if __name__ == "__main__":
    app = App()
    app.mainloop()






