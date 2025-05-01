import time
from grove_rgb_lcd import *

# Clear screen and set to blue
setText("LCD Test Start")
setRGB(0, 0, 255)
time.sleep(1)

while True:
    try:
        # Blink between blue and off every 0.5 seconds
        setText("BLUE ON")
        setRGB(0, 0, 255)
        time.sleep(0.5)

        setText("       ")
        setRGB(0, 0, 0)
        time.sleep(0.5)

    except IOError:
        print("LCD Error")

