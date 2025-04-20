#!/usr/bin/env python3
"""
Crash Alarm for Bike / Car ‑‑ with Simulation Mode
==================================================
This script can now run *either* on real MPU‑6050 hardware *or* in a
self‑contained **--simulate** mode that fabricates realistic accelerometer
readings.  Use the simulation to verify your MQTT pipeline or dashboard when
you don’t have the sensor wired up (or when it intermittently throws the
Remote‑I/O error shown in your screenshot).

  $ python3 crash_alarm.py --mode bike --simulate    # no hardware needed
  $ python3 crash_alarm.py --mode car                # real sensor on I²C

Changes at a glance
-------------------
* New **FakeMPU6050** class generates dictionaries like
  `{ 'x': 0.05, 'y': 0.02, 'z': 9.7 }` every sample.
* `--simulate` flag chooses fake vs. physical sensor.
* Always **prints the raw dictionary** each loop so you can watch the stream
  (exactly like the screenshot) while the crash logic runs in the background.
* Everything else (threshold detection + MQTT alert) is unchanged, so your
dashboard sees the same payload either way.
"""

import argparse
import json
import math
import random
import signal
import sys
import time
from typing import Dict

try:
    from mpu6050 import mpu6050  # Only imported when hardware is used
except ImportError:
    # Library missing on non‑Pi hosts – okay in simulation mode
    mpu6050 = None  # type: ignore

import paho.mqtt.client as mqtt

# ---------------------------------------------------------------------------
# Configuration constants (edit as you like)
# ---------------------------------------------------------------------------
MODES = {
    "bike": {"threshold_g": 2.5, "cooldown": 10},  # softer threshold
    "car":  {"threshold_g": 5.0, "cooldown": 5},   # harsher threshold
}
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT   = 1883
MQTT_TOPIC  = "mydevice/crash"

SAMPLE_HZ = 50   # Hz – sampling rate
SMOOTH_N  = 4    # moving‑average length

# ---------------------------------------------------------------------------
# Fake sensor for --simulate
# ---------------------------------------------------------------------------
class FakeMPU6050:
    """Mimics the public API of mpu6050.mpu6050."""

    GRAVITY = 9.80665  # m/s²

    def __init__(self):
        self._t0 = time.time()

    def get_accel_data(self) -> Dict[str, float]:
        """Return a dict with x,y,z keys, including occasional spikes."""
        # Small vibrations around rest position (z ≈ +g)
        noise = lambda scale: random.uniform(-scale, scale)
        ax = noise(0.2)
        ay = noise(0.2)
        az = self.GRAVITY + noise(0.3)

        # Roughly every 8–12 seconds inject a ‘crash’ spike
        if random.random() < (1 / (SAMPLE_HZ * 10)):
            spike = random.uniform(15, 35)  # 1.5‑3.5 g extra
            axis = random.choice(["x", "y", "z"])
            if axis == "x":
                ax += spike * random.choice([-1, 1])
            elif axis == "y":
                ay += spike * random.choice([-1, 1])
            else:
                az += spike * random.choice([-1, 1])
        return {"x": ax, "y": ay, "z": az}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def send_alert(mode: str, accel_g: float) -> None:
    """Publish JSON payload announcing a crash event."""
    payload = json.dumps({
        "event": "crash",
        "mode": mode,
        "peak_g": round(accel_g, 2),
        "timestamp": time.time(),
    })
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, payload, qos=1)
    client.disconnect()
    print("🚨 MQTT alert sent →", payload)


def accel_magnitude_g(ax: float, ay: float, az: float) -> float:
    """Compute |a| in *g* (not m/s²)."""
    g_ms2 = FakeMPU6050.GRAVITY
    return math.sqrt(ax * ax + ay * ay + az * az) / g_ms2

# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Bike/Car crash detector with optional simulation")
    parser.add_argument("--mode", choices=MODES.keys(), default="bike")
    parser.add_argument("--simulate", action="store_true", help="Use synthetic accelerometer data")
    args = parser.parse_args()

    conf = MODES[args.mode]

    # Choose sensor implementation
    if args.simulate:
        sensor = FakeMPU6050()
    else:
        if mpu6050 is None:
            sys.exit("mpu6050 library not available – run with --simulate or install the lib on Raspberry Pi")
        sensor = mpu6050(0x68)

    history = []
    last_alert = 0.0

    print(f"Mode: {args.mode}  |  Threshold: {conf['threshold_g']} g  |  Simulate: {args.simulate}")

    def _sig_exit(_sig, _frm):
        print("\nExiting cleanly…")
        sys.exit(0)

    signal.signal(signal.SIGINT, _sig_exit)

    interval = 1.0 / SAMPLE_HZ

    while True:
        sample = sensor.get_accel_data()  # {'x':…, 'y':…, 'z':…}
        print(sample)  # ← matches the console screenshot

        # Magnitude in g units
        g_mag = accel_magnitude_g(sample["x"], sample["y"], sample["z"])

        # Simple moving average for robustness
        history.append(g_mag)
        if len(history) > SMOOTH_N:
            history.pop(0)
        g_avg = sum(history) / len(history)

        # Crash detection
        if g_avg > conf["threshold_g"] and time.time() - last_alert > conf["cooldown"]:
            send_alert(args.mode, g_avg)
            last_alert = time.time()

        time.sleep(interval)


if __name__ == "__main__":
    main()
