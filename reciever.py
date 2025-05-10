import paho.mqtt.client as mqtt 
from grove_rgb_lcd import *
import json
import time 

# ------------ Configuration ----------
TIME_INTERVAL = 1
LOST_THRESHOLD = 5 
last_magnitude = None
last_alarm = None
no_data_count = None
new_data = False

# ------------ MQTT Callbacks ----------
def on_connect(client, userdata, flags, rc):
    client.subscribe("louieshe/feeds/250")

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
client.username_pw_set("louieshe", "password")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()


# ------------ Main Loop ------------
while True:
    
    try:
        # format local time
        timestamp = time.localtime()
        real_hour = timestamp.tm_hour + 16
        if real_hour > 24: 
            real_hour = real_hour - 24
        formatted_time = "%02d:%02d:%02d" % (real_hour, timestamp.tm_min, timestamp.tm_sec)
        # Use last known values if no new data
        if new_data and current_magnitude is not None and current_alarm is not None:
            last_magnitude = current_magnitude
            last_alarm = current_alarm
            new_data = False
            no_data_count = 0

        else: no_data_count += 1

        if no_data_count >= LOST_THRESHOLD:
            setRGB(255, 255, 255)
            setText("%s\n%5.2f   LOST" % (formatted_time, 0.0))
            print("LOST")


        elif last_magnitude is not None and last_alarm is not None: 
            rounded_mag = round(current_magnitude, 2)

            print("Magnitude:", current_magnitude)

            # log.append((formatted_time, {"magnitude": current_magnitude}))

            if current_alarm == 1:
                setRGB(255, 0, 0)
                setText("%s\n%5.2f   CRASH" % (formatted_time, rounded_mag))
                print("CRASH")
                time.sleep(1)
            elif current_alarm == 2:
                setRGB(255, 0, 255)
                setText("%s\n%5.2f   STOLEN" % (formatted_time, rounded_mag))
                print("THEFT")
                time.sleep(1)  
            else:
                setRGB(0, 255, 0)
                setText("%s\n%5.2f" % (formatted_time, rounded_mag))
                print("SAFE")

        time.sleep(TIME_INTERVAL)

    except Exception as e:
        print("Error:", e)

