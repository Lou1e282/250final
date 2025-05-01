from mpu6050 import mpu6050 
import paho.mqtt.client as mqtt
import time
import json

# ---- Configuration ---- 
# THRESHOLD = 10.0
MQTT_INTERVAL = 0.5
READ_FREQ = 50
READS_PER_CYCLE = int(MQTT_INTERVAL * READ_FREQ)

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
        magnitudes = []
        for _ in range(READS_PER_CYCLE):
            magnitudes.append(get_accel_magnitude(sensor))
            time.sleep(1/READ_FREQ)

        avg_magnitude = sum(magnitudes) / READS_PER_CYCLE

        entry = {"magnitude": avg_magnitude, "alarm": 0} 

        client.publish("louieshe/feeds/250", json.dumps(entry))
        print(entry)

    except IOError:
        print("IOError")


    time.sleep(MQTT_INTERVAL)
