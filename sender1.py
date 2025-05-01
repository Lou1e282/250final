from mpu6050 import mpu6050 
import paho.mqtt.client as mqtt
import time
import json

THRESHOLD = 20.0
SAMPLE_INTERVAL = 1

def get_accel_magnitude(sensor):
    accel = sensor.get_accel_data()
    mag = (accel['x']**2 + accel['y']**2 + accel['z']**2) ** 0.5 
    return mag
def on_connect(client, userdata, flags, rc):
   client.subscribe("louieshe/feed/250")
 
client = mqtt.Client()
client.username_pw_set("louieshe", "aio_TVDC93n0PNSAVjPWFOVzWGoTwkaF")
client.on_connect = on_connect
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

if __name__ == "__main__":
    sensor = mpu6050(0x68)

while True: 
    try: 
        magnitude = get_accel_magnitude(sensor)
        alarm = 1 if magnitude > THRESHOLD else 0

        client.publish("louieshe/feeds/alarm", json.dumps({"alarm": alarm, "magnitude": magnitude}))

        print({"magnitude": magnitude, "alarm": alarm})

    except IOError:
        print("IOError")

    time.sleep(SAMPLE_INTERVAL)

