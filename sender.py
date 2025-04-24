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

def on_message(client, userdata, msg):
    print(json.loads(msg.payload.decode()))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("io.adafruit.com", 1883, 60)
client.loop_forever()

if __name__ == "__main__":
    sensor = mpu6050(0x68)

while True: 
    try: 
        magnitude = get_accel_magnitude(sensor)
        timestamp = time.time()
        entry = {"timestamp": timestamp, "magnitude": magnitude, "alarm": 0} 

        if magnitude > THRESHOLD:
            # ---------- buzzz ----------------
            entry = {"timestamp": timestamp, "magnitude": magnitude, "alarm": 1} 
            print(f"{timestamp:.2f}: {magnitude:.2f}, Alarm triggered")
        else:
            print(f"{timestamp:.2f}: {magnitude:.2f}, Safe") 

        client.publish("louieshe/250", json.dumps(entry))

    except IOError:
        print("IOError")


    time.sleep(SAMPLE_INTERVAL)







    

    

