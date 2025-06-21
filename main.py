import os
from datetime import datetime
from datetime import timedelta
import asyncio
from aiohttp import web

from pysphero.utils import toy_scanner
from pysphero.core import Sphero
from pysphero.device_api.user_io import Color
from pysphero.constants import Toy
from pysphero.bluetooth.bluepy_adapter import BluepyAdapter
from pysphero.driving import Direction

#options - get current time 
#set timer
#pomodoro mode

currentDir  = os.getcwd()
routes = web.RouteTableDef()

#1 - home 2- pomodoro 3 clock 4 pomodoro post
@routes.get("/")
async def onHome(request : web.Request):
    request.app['currentStatus'] = 1
    return web.Response(text=open("index.html").read(), content_type="text/html")

@routes.get("/pomodoro")
async def onPomodoro(request : web.Request):
    request.app['currentStatus'] = 2
    return web.Response(text=open("pomodoro.html").read(), content_type="text/html")

@routes.post("/pomodoro")
async def onPomodoroPost(request : web.Request):
    request.app['startTime'] = datetime.now()
    body = await  request.post()
    print("BODY REPS")
    print(body.get("study"))
    request.app['pomodoroCycle'] = 1
    currentTime = datetime.now()
    studyVect = []
    for i in range(0, int(body.get('reps'))):
        currentTime += timedelta(minutes=float(body.get('study')))
        studyVect.append(currentTime)
        currentTime += timedelta(minutes=float(body.get('rest')))
        studyVect.append(currentTime)
    request.app['pomodoro'] = studyVect
    await asyncio.sleep(0.2)
    request.app['currentStatus'] = 4
    return web.Response(text="<a href='/'>Go back to home</a>", content_type="text/html")
@routes.get("/clock")
async def onClock(request : web.Request):
    request.app['currentStatus'] = 3
    return web.Response(text="<a href='/'>Go back to home</a>", content_type="text/html")

async def clockMode(app : web.Application):
    mac_address = "C7:7A:B3:81:35:0C"
    with Sphero(mac_address=mac_address) as sphero:
        await asyncio.sleep(2)
        sphero.power.wake()
        await asyncio.sleep(2)
        sphero.driving.drive_with_heading(speed=0,heading=120)

        while True:
            currentStatus = app['currentStatus']
            if currentStatus == 3:
                print(datetime.now().strftime("%H:%M"))
                sphero.user_io.set_led_matrix_text_scrolling(string=datetime.now().strftime("%H:%M"), color=Color(255,255,255), repeat=False)
                await asyncio.sleep(5)

            elif currentStatus == 4:
                pomodoro = app['pomodoro']
                await asyncio.sleep(0.2)
                pomodoroCycle = app['pomodoroCycle']
                if len(pomodoro) > pomodoroCycle-1:
                    cycleTime = pomodoro[pomodoroCycle - 1]
                    remainingTime= cycleTime - datetime.now()
                    print(remainingTime.total_seconds()/60)
                    if remainingTime.total_seconds() <= 0:
                        app['pomodoroCycle'] += 1
                        print(app['pomodoroCycle'])
                    if pomodoroCycle % 2 != 0:
                        sphero.user_io.set_led_matrix_one_color(color=Color(green=255))
                        await asyncio.sleep(2)
                    else:
                        sphero.user_io.set_led_matrix_one_color(color=Color(blue=255))
                        await asyncio.sleep(2)
                else:
                    sphero.user_io.set_led_matrix_text_scrolling(string="Done!", color=Color(255,255,255), repeat=False)

                    await asyncio.sleep(4)

            await asyncio.sleep(0.2)

async def startServer(app : web.Application):
    mac_address = "C7:7A:B3:81:35:0C"
    #sphero = Sphero(mac_address=mac_address)
    #with Sphero(mac_address=mac_address) as sphero:
        #$await asyncio.sleep(2)
        #sphero.power.wake()
        #app['sphero'] = sphero

 
    app['pomodoroCycle'] = 0
    app['currentStatus'] = 0
    app['pomodoro'] = []
    app['server'] = asyncio.create_task(clockMode(app))



app = web.Application()
_ = app.router.add_static('/public', path=currentDir + "/public", name='public')
_ = app.add_routes(routes)
app.on_startup.append(startServer)
web.run_app(app=app,port=3000)

