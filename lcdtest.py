from grovepi import *
from grove_rgb_lcd import *
import time

if __name__ == "__main__":
    try:
        while True:
            setRGB(0, 0, 255)          # Set to blue
            setText("BLUE BLINK ON")
            time.sleep(0.5)

            setRGB(0, 0, 0)            # Turn off backlight
            setText("                ")  # Clear text
            time.sleep(0.5)

    except KeyboardInterrupt:
        setText("Stopped")
        setRGB(0, 0, 0)

