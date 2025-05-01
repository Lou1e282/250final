from mpu6050 import mpu6050 
import paho.mqtt.client as mqtt
import time
import json

THRESHOLD = 20.0
SAMPLE_INTERVAL = 0.1

def get_accel_magnitude(sensor):
    accel = sensor.get_accel_data()
    mag = (accel['x']**2 + accel['y']**2 + accel['z']**2) ** 0.5 
    return mag

client = mqtt.Client()
client.username_pw_set("louieshe", "aio_TVDC93n0PNSAVjPWFOVzWGoTwkaF")
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

if __name__ == "__main__":
    sensor = mpu6050(0x68)

next_status = time.monotonic() + 0.5
next_heartbeat = time.monotonic() + 6
last_magnitude = 0

while True: 
    try: 
        now = time.monotonic()
        magnitude = get_accel_magnitude(sensor)

        # status
        if now >= next_status: 
            status = {"magnitude": magnitude}
            client.publish("louieshe/feeds/250.status", json.dumps(status))
            next_status = now + 0.5

        # heartbeat
        if now >= next_heartbeat:
            heartbeat = {"heartbeat": 1}
            client.publish("louieshe/feeds/250.heartbeat", json.dumps(heartbeat))
            next_heartbeat = now + 6
        # crash
        if abs(magnitude - last_magnitude) > THRESHOLD:
            entry = {"magnitude": magnitude, "alarm": 1}
            client.publish("louieshe/feeds/250.crash", json.dumps(entry))
            print(entry)
        # theft
        if magnitude > 2.0 and last_magnitude < 0.5:
            theft = {"magnitude": magnitude, "alarm": 1}
            client.publish("louieshe/feeds/250.theft", json.dumps(theft))
            print(theft)

    except IOError:
        print("IOError")

    last_magnitude = magnitude
    time.sleep(SAMPLE_INTERVAL)
