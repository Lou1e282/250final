import paho.mqtt.client as mqtt 
from grove_rgb_lcd import *
import json
import time 

# ------------ Configuration ----------
TIME_INTERVAL = 1
CRASH_THRESHOLD = 5 
current_magnitude = None
current_alarm = None
new_data = False

# ------------ MQTT Callbacks ----------
def on_connect(client, userdata, flags, rc):
    client.subscribe("louieshe/feeds/alarm")

def on_message(client, userdata, msg):
    global current_magnitude, current_alarm, new_data
    try:
        payload = json.loads(msg.payload.decode())
        current_alarm = payload.get("alarm", 0)
        current_magnitude = payload.get("magnitude", 0)
        new_data = True
    except json.JSONDecodeError:
        pass

def on_disconnect(client, userdata, rc):
    print("Disconnected")

# ------------ MQTT Setup ----------
client = mqtt.Client()
client.username_pw_set("louieshe", "")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

# ------------ Main Loop ------------
log = []
# wakes sender


while True:
    if new_data and current_magnitude is not None and current_alarm is not None:
        try:
            timestamp = time.localtime()
            formatted_time = "%02d:%02d:%02d" % (timestamp.tm_hour + 16, timestamp.tm_min, timestamp.tm_sec)
            rounded_mag = round(current_magnitude, 2)

            print("Magnitude:", current_magnitude)

            log.append((formatted_time, {"magnitude": current_magnitude}))

            # crash detection: compare consecutative acceleration difference
            if len(log) >= 2:
                prev_mag = log[-2][1].get("magnitude", 0)
                
                if abs(current_magnitude - prev_mag) > CRASH_THRESHOLD:
                    setRGB(255, 0, 0)
                    setText("%s\n%5.2f    CRASH" % (formatted_time, rounded_mag))
                    print("CRASH DETECTED")
                    time.sleep(1)
                else:
                    setRGB(0, 255, 0)
                    setText("%s\n%5.2f" % (formatted_time, rounded_mag))
                    print("SAFE")

            new_data = False  # Reset after handling

        except Exception as e:
            print("Error:", e)

    time.sleep(TIME_INTERVAL)

