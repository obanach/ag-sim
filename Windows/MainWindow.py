import customtkinter
import Frames.HubFrame as Frames
import Windows.AddNewHubWindow as hub
import Entities.GlobalVariables as gv
import requests

class App(customtkinter.CTk):
    def __init__(self):
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
        self.CreateHubButton.grid(column=1, row=0, sticky='nesw')
        self.DeleteHubButton.grid(column=0, row=0, sticky='wnse')
        self.TabView.grid(column=0, columnspan=2, row=1, sticky='wesn')

    def AddNewHubCallback(self):
        hub.AddNewHubWindow(self)

    def DeleteHubCallback(self):
        toDelete = self.TabView.get()

        if not toDelete:
            return
        
        self.TabView.delete(toDelete)

        #TODO zrobić magie z API potem

    def updateHubList(self, hub):
        parameters = {'pairCode': hub.PairCode}
        response = requests.post(url=gv.GlobalVariables.PairHubEndpoint(), json=parameters)
        data = response.json()
        # print(data['name'])
        self.TabView.add(f"Hub: {data['name']}")
        self.Hub = Frames.HubFrame(self.TabView.tab(f"Hub: {data['name']}"))
        self.Hub.pack(expand=True, fill='both')
        # self.Hub.grid(row=1, column=0, sticky='news')
        #TODO
        # parowanie clienta poprze endpoint -> post /hub/pair
        # w odpowiedzi są dane do mqtt oraz token
        pass