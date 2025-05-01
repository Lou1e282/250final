import paho.mqtt.client as mqtt 
from grove_rgb_lcd import *
import sys
import json
import time 

# ------------ Configuration ----------
TIME_INTERVAL = 0.5
current_msg = None  # Initialize it globally

# ------------ MQTT Callbacks ----------
def on_connect(client, userdata, flags, rc):
    client.subscribe("louieshe/feeds/magnitude")
    client.subscribe("louieshe/feeds/alarm")

def on_message(client, userdata, msg):
    global current_msg
    try:
        current_msg = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        current_msg = None

def on_disconnect(client, userdata, rc):
    print("Disconnected")

# ------------ MQTT Setup ----------
client = mqtt.Client()
client.username_pw_set("louieshe", "aio_TVDC93n0PNSAVjPWFOVzWGoTwkaF")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

# ------------ Mock display functions (if grove not used) ------------
def setText(text):
    print("LCD:", text)

def setRGB(r, g, b):
    print("RGB Color:", r, g, b)

# ------------ Main Loop ------------
log = [] 
error_log = []

while True:
    if current_msg:
        try:
            timestamp = time.localtime()
            formatted_time = "%02d:%02d:%02d" % (timestamp.tm_hour, timestamp.tm_min, timestamp.tm_sec)
            magnitude = current_msg.get("magnitude", 0)
            rounded_mag = round(magnitude, 2)
            alarm = current_msg.get("alarm", 0)

            print("Magnitude:", magnitude)

            log.append((formatted_time, current_msg))

            if alarm == 1:
                setRGB(255, 0, 0)
                setText("%s\n%5.2f        DANGER" % (formatted_time, rounded_mag))
                print("ALARM TRIGGERED")
                time.sleep(1)
            else:
                setRGB(0, 255, 0)
                setText("%s\n%5.2f" % (formatted_time, rounded_mag))
                print("SAFE")

            # crash detection
            if len(log) >= 2:
                prev_mag = log[-2][1].get("magnitude", 0)
                if abs(magnitude - prev_mag) > 20:
                    print("CRASH DETECTED")

        except Exception as e:
            print("Error:", e)

    time.sleep(TIME_INTERVAL)
