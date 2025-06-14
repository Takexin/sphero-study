import time
from datetime import datetime
import aiohttp
import asyncio
#options - get current time 
#set timer
#pomodoro mode
while True:
  print(datetime.now().strftime("%H:%M"))
  time.sleep(0.2)

async def handler(request):
  pass

app = web.Application()

