import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    client.subscribe("louieshe/250")

def on_message(client, userdata, msg):
    print(json.loads(msg.payload.decode()))

client = mqtt.Client()
client.username_pw_set("louieshe", "aio_QkNz07b4Jbyp4xAH7VIcxKl2GnIz")
client.on_connect = on_connect
client.on_message = on_message
client.connect("io.adafruit.com", 1883, 60)
client.loop_forever()

