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

# # mqtt publishing
# def on_connect(client, userdata, flags, rc):

#     print("Connected to server (i.e., broker) with result code "+str(rc))
#     client.subscribe("louieshe/250")

#     #Add the custom callbacks by indicating the topic and the name of the callback handle
#     client.message_callback_add("louieshe/250", on_message_from_ping) # -- 

# def on_message(client, userdata, msg):
#     print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

# #Custom message callback. info
# def on_message_from_ping(client, userdata, message):

#    num = (message.payload.decode())+ 1

#    print(f"Custom callback - num {num}")


client = mqtt.Client()
client.username_pw_set("your_username", "your_aio_key")
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()

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







    

    

