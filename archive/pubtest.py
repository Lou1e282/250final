import paho.mqtt.client as mqtt
import time
import json

client = mqtt.Client()
client.username_pw_set("louieshe", "aio_QkNz07b4Jbyp4xAH7VIcxKl2GnIz")
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

while True:
    data = {"value": time.time()}
    client.publish("louieshe/feeds/250", json.dumps(data))
    time.sleep(0.5)