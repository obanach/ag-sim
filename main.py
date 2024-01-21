import Windows.MainWindow as main
import asyncio
from threading import Thread

if __name__ == "__main__":
    def StartAsyncioLoop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    asyncioLoop = asyncio.new_event_loop()
    t = Thread(target=StartAsyncioLoop, args=(asyncioLoop,))
    t.start()
    
    app = main.App(asyncioLoop)
    app.mainloop()
    app.SaveHubs()
    asyncioLoop.call_soon_threadsafe(asyncioLoop.stop)
    t.join()