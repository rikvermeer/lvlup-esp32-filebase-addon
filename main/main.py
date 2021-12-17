import uasyncio
from main.config import Config

cfg = Config()

class Runner(object):
    async def run_forever(self):
        while True:
            #print('hello')
            await uasyncio.sleep_ms(500)

async def main():
   runner = Runner()  # Constructor creates tasks
   await runner.run_forever()  # Never terminates

def run():  # Entry point
    while True:
        try:
            uasyncio.run(main())
        finally:
            uasyncio.new_event_loop()
        
run()
