import os
import json
from datetime import datetime
from datetime import timedelta
import asyncio
from aiohttp import web

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
    request.app['currentStatus'] = 4
    request.app['startTime'] = datetime.now()
    body = await  request.post()
    print("BODY REPS")
    print(body.get("study"))
    request.app['pomodoroReps'] = body.get('reps')
    request.app['pomodoroStudy'] = body.get('study')
    request.app['pomodoroRest'] = body.get('rest')
    request.app['pomodoroCycle'] = 1

    return web.Response(text="okay")
@routes.get("/clock")
async def onClock(request : web.Request):
    request.app['currentStatus'] = 3
    return web.Response(text="<a href='/'>Go back to home</a>", content_type="text/html")

async def clockMode(app : web.Application):
    while True:
        currentStatus = app['currentStatus']
        if currentStatus == 3:
            print(datetime.now().strftime("%H:%M"))
        elif currentStatus == 4:
            if app['pomodoroReps'] != app['pomodoroCycle']:
                cycleTime = (app['startTime'] + timedelta(minutes=float(app['pomodoroStudy'])*int(app['pomodoroCycle']))) 
                remainingStudyTime = cycleTime - datetime.now()
                print(remainingStudyTime.total_seconds()/60)
                if remainingStudyTime.total_seconds() <= 0:
                    pass
                    #remainingRestTime = 

        await asyncio.sleep(0.2)

async def startServer(app : web.Application):
    app['pomodoroReps'] = 0
    app['pomodoroStudy'] = 0
    app['pomodoroRest'] = 0
    app['pomodorostartTime'] = 0
    app['pomodoroCycle'] = 0
    app['currentStatus'] = 0
    app['server'] = asyncio.create_task(clockMode(app))



app = web.Application()
_ = app.router.add_static('/public', path=currentDir + "/public", name='public')
_ = app.add_routes(routes)
app.on_startup.append(startServer)
web.run_app(app=app,port=3000)

