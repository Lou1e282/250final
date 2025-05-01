import paho.mqtt.client as mqtt 
# from flask import flask
import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
# import grovepi
# from grove_rgb_lcd import * 
import json
import time 

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
client.loop_start()

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
            timestamp = time.localtime()
            formatted_time = "%02d:%02d:%02d" % (timestamp.tm_hour, timestamp.tm_min, timestamp.tm_sec)
            magnitude = current_msg.get("magnitude")
            rounded_mag = round(magnitude, 2)
            alarm = current_msg.get("alarm")

            print("Magnitude:", magnitude)

            log.append(timestamp, current_msg)

            if alarm == 1:
                setRGB(255, 0, 0)
                setText("%s\n%5.2f        DANGER" % (formatted_time, rounded_mag))
                # buzzer
                print("ALARM TRIGGERED")
                # error_log.append((magnitude))
                time.sleep(1)
                
            else:
                setRGB(0, 255, 0)
                setText("%s\n%5.2f" % (formatted_time, rounded_mag))
                print("SAFE")


            # crash detect 
            if log[-1][1] - log[-2][1] > 20:
                print("crashed")

    
        except IOError:
            print("IOError")

        if i == 2 :# button pressed:
            with open("accel_log.txt", "w") as f:
                for entry in log:
                    f.write(json.dumps(entry)+"\n")
            print("Logged")
            time.sleep(0.5) # debounce
    
    time.sleep(TIME_INTERVAL)


        


        

    
 
    
    



            
    