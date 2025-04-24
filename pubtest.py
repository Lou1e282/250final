import paho.mqtt.client as mqtt
import time
import json

client = mqtt.Client()
client.username_pw_set("your_username", "your_aio_key")
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

while True:
    data = {"value": time.time()}
    client.publish("your_username/feeds/test", json.dumps(data))
    time.sleep(2)
