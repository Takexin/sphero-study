import pygatt
from pysphero.core import Sphero
from pysphero.device_api.user_io import Color
from time import sleep

adapter = pygatt.GATTToolBackend()
mac_address = "C7:7A:B3:81:35:0C"



# Replace with your actual MAC address

# Initialize pygatt GATT backend
adapter = pygatt.GATTToolBackend()

try:
    print("Starting BLE adapter...")
    adapter.start()

    print(f"Connecting to {mac_address}...")
    # Connect via pygatt
    bolt = SpheroBolt(adapter=adapter, mac_address=mac_address)

    # Let the BLE stack stabilize
    sleep(2)

    print("Pinging Sphero...")
    bolt.ping()
    sleep(0.5)

    print("Setting LED matrix color...")
    bolt.user_io.set_led_matrix_one_color(color=Color(blue=255))

finally:
    print("Stopping BLE adapter.")
    try:
        adapter.stop()
    except Exception as e:
        print("Warning during adapter stop:", e)

