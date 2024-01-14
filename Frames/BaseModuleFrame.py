import customtkinter
import threading
import asyncio
import uuid

class HubFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.Id = uuid.uuid4()
        self.moduleName = "Costam"
        self.DataFrequency = 10
        self.DataNames = ["costam"]
        self.DataLowerBound = [10]
        self.DataUpperBound =[100]
        self.DataTask = asyncio.create_task(self.SendData(self))

    async def SendData(self):
        try:
            while True:
                #TODO: dodać klasę Api do wysyłania danych do endpointów
                await asyncio.sleep(self.DataFrequency)
        except asyncio.CancelledError:
            return

    async def __del__(self):
        self.DataTask.cancel()
