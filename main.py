import time 
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI 
from spherov2.types import Color 

toy = scanner.find_toy()

with SpheroEduAPI(toy) as droid:
    print("toy found")
    droid.set_main_led(Color(0,0,255))
    #test of the sphero bot
    time.sleep(2)

