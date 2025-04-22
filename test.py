from mpu6050 import mpu6050 
import time

def get_accel_magnitude(sensor):
    accel = sensor.get_accel_data()
    mag = (accel['x']**2 + accel['y']**2 + accel['z']**2) ** 0.5 

    return mag


if __name__ == "__main__":
    sensor = mpu6050(0x68)

    log = []

    while True: 
        magnitude = get_accel_magnitude(sensor)
        timestamp = time.time()
        log.append((timestamp, magnitude))
        print(f"{timestamp:.2f}: {mag:.2f} ")
        time.sleep(0.5)







    

    

