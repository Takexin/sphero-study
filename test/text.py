import time
from pysphero.utils import toy_scanner
from pysphero.core import Sphero
from pysphero.device_api.user_io import Color
from pysphero.constants import Toy
from pysphero.bluetooth.bluepy_adapter import BluepyAdapter

def main():
    mac_address = "C7:7A:B3:81:35:0C"
    with Sphero(mac_address=mac_address) as sphero:
        time.sleep(2)
        sphero.power.wake()
        time.sleep(2)
        #sphero.user_io.set_led_matrix_single_character(symbol="0", color=Color(255,255,255))

        sphero.user_io.set_led_matrix_text_scrolling(string="00:00", color=Color(255,255,255), repeat=False)
        time.sleep(2)
        sphero.user_io.set_led_matrix_one_color(color=Color())
        time.sleep(2)
        sphero.power.enter_soft_sleep()
        print("done")

if __name__ == "__main__":
    main()
