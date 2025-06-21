import time
from pysphero.utils import toy_scanner
from pysphero.device_api.user_io import Color

def main():
    with toy_scanner() as sphero:
        sphero.power.wake()
        time.sleep(2)
        sphero.user_io.set_lead_matrix_one_color(color=Color(blue=255))
        time.sleep(2)
        print("done")

if __name__ == "__main__":
    main()
