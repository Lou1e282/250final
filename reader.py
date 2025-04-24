import paho.mqtt.client as mqtt
# import grovepi
# from grove_rgb_lcd import * 
from flask import flask
import json


# Call back when client connects
def on_connect(client, userdata, flags, rc):
    # print("Connected with result code " + str(rc))
    client.subscribe("louieshe/250") 

def on_message(client, userdata, msg):
     global latest_msg
     try:
        latest_msg = json.loads(msg.payload.decode())
     except json.JSONDecodeError:
        latest_msg = None
    
# -------MQTT-------------
client = mqtt.Client()
client.username_pw_set("your_username", "your_aio_key")
client.on_connect = on_connect
client.on_message = on_message
client.connect("io.adafruit.com", 1883, 60)
client.loop_forever()    # main threa

# Clear lcd
setText("")

if __name__ == "__main__":
    errorlog = [] 
    log = []
    while True:
        try:
            timestamp = data.get("timestamp")
            magnitude = data.get("magnitude")
            alarm = data.get("alarm")

            print(f"Time: {timestamp}, Magnitude: {magnitude}")
            log.append(timestamp, magnitude) 

            if alarm == 1:
                setRGB(255, 0, 0)
                setText("%d , %d \n DANGER!!!" % (timestamp, magnitude))
                errorlog.append(timestamp, magnitude)
                time.sleep(3)

            else:
                setRGB(0, 255, 0)
                setText("%d , %d " % (timestamp, magnitude))
        
        except IOError:
            print("IOError")
        
        time.sleep(0.4)


        


        

    
 
    
    



            
    