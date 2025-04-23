import paho.mqtt.client as mqtt
import grovepi
from grove_rgb_lcd import * 

# Call back when client connects
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("louieshe/250") 

# Callback when a message is received
def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + str(msg.payload.decode()))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker (replace with your broker address)
client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()

# Clear lcd
setText("")
setRGB(0,0,255)

while True:
    try: 
        if alarm_triggered: # there is alarm
           setRGB(255, 0, 0)
           setText("%d G\n DANGER!!!" %(mag))
        else:
           setRGB(0, 0, 255)
           setText("%d G" % (mag))
    except IOError:
        print("IOError")
            
    