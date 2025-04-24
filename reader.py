import paho.mqtt.client as mqtt 
# from flask import flask
import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
# import grovepi
# from grove_rgb_lcd import * 
import json
import time
import os

# ------------ Configuration ----------
TIME_INTERVAL = 0.5

def on_connect(client, userdata, flags, rc):
    client.subscribe("louieshe/feeds/250")

def on_message(client, userdata, msg):
    global current_msg
    try:
        current_msg = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        current_msg = None

def on_disconnect(client, userdata, rc):
    print("Disconnected")

client = mqtt.Client()
client.username_pw_set("louieshe", "aio_xvPv56CV8Yyv3Vz9B7CDo0BSEK83")
client.on_connect = on_connect
client.on_message = on_message
client.connect("io.adafruit.com", 1883, 60)
client.loop_forever()

# ------------ lcd ------------
# clear
setText("")


if __name__ == "__main__":
    #include error loging
    log = [] 
    error_log = []

while True:
    if current_msg:
        try:
            realtime = time.localtime()
            magnitude = current_msg.get("magnitude")
            alarm = current_msg.get("alarm")

            print("Magnitude:", magnitude)

            log.append(realtime, current_msg)

            if alarm == 1:
                setRGB(255, 0, 0)
                setText("%d g\n DANGER" %(magnitude))

                # buzzer
                print("ALARM TRIGGERED")
                error_log.append((magnitude))
                time.sleep(1)
            else:
                setRGB(0, 255, 0)
                setText("%d g\n DANGER" %(magnitude))
                print("SAFE")

                current_msg = None  # Clear after processing
        except IOError:
            print("IOError")

        if i == 2 :# button pressed:
            with open("accel_log.txt", "w") as f:
                for entry in log:
                    f.write(json.dumps(entry)+"\n")
            print("Logged")
            time.sleep(0.5) # debounce
    
    time.sleep(TIME_INTERVAL)


        


        

    
 
    
    



            
    