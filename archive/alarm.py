import json
import time
import math

from mpu6050 import mpu6050
import paho.mqtt.client as mqtt

MODES = {
    "bike": {"threshold_g": 2.5, "cooldown": 10}, 
    "car": {"threshold_g": 5.5, "cooldown": 5}, 
}

#-----------mqtt codes 


def send_alert(mode: str, accel_g: float) -> None: 
    """publish crash"""
    payload = json.dumps ({
        "event": "crash",
        "mode": mode,
        "peak_g" round(accel_g, 2),
        "timestamp": time.time(), 
    })

    client = mqtt.client()
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, payload, qos=1)
    client.disconnect()
    print(" Crash alert sent →", payload)
    
def accel_magnitude(sensor: mpu6050) -> float:
    """return acceleration vector magnitude in g"""
    data = sensor.get_accel_data()
    ax, ay, az = data["x"], data["y"], data["z"]
    return math.sqrt(ax * ax + ay * ay + az * az)

def main() -> None:
    parser = argparse.ArgumentParser(description="Bike/Car crash detector")
    parser.add_argument("--mode", choices=MODES.keys(), default="bike")
    args = parser.parse_args()
    conf = MODES[args.mode]

    sensor = mpu6050(0x68)
    history = []  # last N magnitudes for smoothing
    last_alert_time = 0.0

    print(f"Mode: {args.mode}  |  Threshold: {conf['threshold_g']} g")

    def _exit_handler(sig, _):
        print("\nExiting cleanly…")
        sys.exit(0)

    signal.signal(signal.SIGINT, _exit_handler)

    interval = 1.0 / SAMPLE_HZ
    while True:
        g = accel_magnitude(sensor)
        history.append(g)
        if len(history) > SMOOTH_N:
            history.pop(0)
        g_avg = sum(history) / len(history)

        if (g_avg > conf["threshold_g"] and
                time.time() - last_alert_time > conf["cooldown"]):
            send_alert(args.mode, g_avg)
            last_alert_time = time.time()
        time.sleep(interval)


if __name__ == "__main__":
    main()