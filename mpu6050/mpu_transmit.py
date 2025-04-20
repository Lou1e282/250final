import paho.mqtt.client as mqtt
import smbus
import json
import time

# adafruit api
AIO_USERNAME = "your_adafruit_username"
AIO_KEY = "your_aio_key"

client = mqtt.Client()
client.userame_pw_set(AIO_USERNAME, AIO_KEY)
client.connect("io.adafruit.com", 1883, 60)


while True:
    data = mpu6050.get_all_data()   # read from mpu6050 

    payload = json.dumps(data)

   # Publish to a feed
    client.publish(f"{AIO_USERNAME}/feeds/gyro", payload) # depends on the feed 
    time.sleep(0.01) 
    

