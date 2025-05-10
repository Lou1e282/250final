from mpu6050 import mpu6050 
import paho.mqtt.client as mqtt
import time
import json

# ---- Configuration ---- 
ACCEL_THRESHOLD = 20.0
VAR_THRESHOLD = 3.5
VAR_DURATION = 15
MQTT_INTERVAL = 1
READ_FREQ = 20
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
client.username_pw_set("louieshe", "password") # space holding pasword
client.on_connect = on_connect
client.connect("io.adafruit.com", 1883, 60)
client.loop_start()



#  -------------- Main loop ---------------------
if __name__ == "__main__":
    sensor = mpu6050(0x68)

# Sliding window for theft variance
variances = []

while True: 
    try: 
        magnitudes = []
        alarm_flag = 0

        for _ in range(READS_PER_CYCLE):
            mag = get_accel_magnitude(sensor)
            magnitudes.append(mag)
            if mag > ACCEL_THRESHOLD:
                alarm_flag = 1  # immediate crash
            time.sleep(1 / READ_FREQ)

        avg_magnitude = sum(magnitudes) / READS_PER_CYCLE
        squared_diffs = [(x - avg_magnitude) ** 2 for x in magnitudes]
        variance = sum(squared_diffs) / READS_PER_CYCLE

        #  rolling window in detecting theft
        variances.append(variance)
        if len(variances) > VAR_DURATION:
            variances.pop(0)

        if alarm_flag == 0 and len(variances) == VAR_DURATION:
            avg_variance = sum(variances) / VAR_DURATION
            if avg_variance > VAR_THRESHOLD:
                alarm_flag = 2  # theft (overrides crashs)

        entry = {"magnitude": avg_magnitude, "alarm": alarm_flag}
        client.publish("louieshe/feeds/250", json.dumps(entry))
        print(entry)

    except IOError:
        print("IOError")

    time.sleep(MQTT_INTERVAL)
