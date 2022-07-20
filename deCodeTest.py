import os
import numpy as np
import re

debug = True

def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)

with open("testRead.txt", 'r') as ser:

    while True:
        line=ser.readline()   
        buffer = re.findall('....?', line)
        
        if debug:
            print("Receiving ", len(buffer), "sets of data.")
        
        if not line:
            break

        if(len(buffer) == 14):  # confirm the length of the data, should be 14 set of values.
            # the first IMU's data
            rawAccX = s16(int(buffer[0], 16))
            rawAccY = s16(int(buffer[1], 16))
            rawAccZ = s16(int(buffer[2], 16))

            rawTemp = s16(int(buffer[3], 16))

            rawGyroX = s16(int(buffer[4], 16))
            rawGyroY = s16(int(buffer[5], 16))
            rawGyroZ = s16(int(buffer[6], 16))

            accel_scale = 8192.0  #MPU6050_RANGE_4_G
            # setup range dependant scaling
            accX = rawAccX / accel_scale
            accY = rawAccY / accel_scale
            accZ = rawAccZ / accel_scale

            gyro_scale = 65.5 # MPU6050_RANGE_500_DEG
            gyroX = rawGyroX / gyro_scale
            gyroY = rawGyroY / gyro_scale
            gyroZ = rawGyroZ / gyro_scale

            temperature = (rawTemp / 340.0) + 36.53
            if debug:
                print("The first IMU's data: {0}, {1}, {2}, {3}, {4}, {5}, {6}".format(accX, accY, accZ, gyroX, gyroY, gyroZ, temperature))

            # the second IMU's data
            rawAccX = s16(int(buffer[7], 16))
            rawAccY = s16(int(buffer[8], 16))
            rawAccZ = s16(int(buffer[9], 16))

            rawTemp = s16(int(buffer[10], 16))

            rawGyroX = s16(int(buffer[11], 16))
            rawGyroY = s16(int(buffer[12], 16))
            rawGyroZ = s16(int(buffer[13], 16))

            accel_scale = 8192.0  #MPU6050_RANGE_4_G
            # setup range dependant scaling
            accX = rawAccX / accel_scale
            accY = rawAccY / accel_scale
            accZ = rawAccZ / accel_scale

            gyro_scale = 65.5 # MPU6050_RANGE_500_DEG
            gyroX = rawGyroX / gyro_scale
            gyroY = rawGyroY / gyro_scale
            gyroZ = rawGyroZ / gyro_scale

            temperature = (rawTemp / 340.0) + 36.53
            if debug:
                print("The second IMU's data: {0}, {1}, {2}, {3}, {4}, {5}, {6}".format(accX, accY, accZ, gyroX, gyroY, gyroZ, temperature))



