from mpu6050 import mpu6050 
import paho.mqtt.client as mqtt
import time
import json

# ---- Configuration ---- 
THRESHOLD = 20.0
SAMPLE_INTERVAL = 0.5

# read acceleration magnitude from sensor
def get_accel_magnitude(sensor):
    accel = sensor.get_accel_data()
    mag = (accel['x']**2 + accel['y']**2 + accel['z']**2) ** 0.5 

    return mag

# ---------- mqtt publishing --------------
def on_connect(client, userdata, flags, rc):
    client.subscribe("louieshe/feeds/250")

client = mqtt.Client()
client.username_pw_set("louieshe", "")
client.on_connect = on_connect
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

if __name__ == "__main__":
    sensor = mpu6050(0x68)

while True: 
    try: 
        magnitude = get_accel_magnitude(sensor)
        entry = {"magnitude": magnitude, "alarm": 0} 

        if magnitude > THRESHOLD:
            # buzzer
            entry = {"magnitude": magnitude, "alarm": 1} 

        client.publish("louieshe/feeds/250", json.dumps(entry))
        print(entry)

    except IOError:
        print("IOError")


    time.sleep(SAMPLE_INTERVAL)
