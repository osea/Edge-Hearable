import numpy as np
import serial
import re
import time
import csv

debug = True

def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)

if __name__ == '__main__':
        
    #initialize serial port
    ser = serial.Serial()
    ser.port = '/dev/tty.usbmodem11101' #Arduino serial port, should change accrodingly
    ser.baudrate = 115200
    ser.timeout = 10 

    ser.open()
    if ser.is_open==True:
        print("\nAll right, serial port now open. Configuration:\n")
        print(ser, "\n") 

    start_time = time.time()
    now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
    
    with open("./logs/"+now+r"_imu.csv", 'w') as imuFile:
        imuFile.write("timestamp" + "," + "accX_l" + "," + "accY_l" + "," + "accZ_l" + "," + "gyroX_l"+ "," + "gyroY_l" + "," + "gyroZ_l"  + "," + "temp_l" + "," + "accX_r" + "," + "accY_r" + "," + "accZ_r" + "," + "gyroX_r"+ "," + "gyroY_r" + "," + "gyroZ_r"  + "," + "temp_r" + "\n") 

        while True:
            line=ser.readline()

            if debug:
                print(line)   

            if "Failed" in str(line):
                print("Please restart!") 
                break
            
            try:
                decodeStr = line.decode()
            except:
                print("Invaild string.")
                continue

            buffer = re.findall('....?',decodeStr)

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
                accX_l = rawAccX / accel_scale
                accY_l = rawAccY / accel_scale
                accZ_l = rawAccZ / accel_scale

                gyro_scale = 65.5 # MPU6050_RANGE_500_DEG
                gyroX_l = rawGyroX / gyro_scale
                gyroY_l = rawGyroY / gyro_scale
                gyroZ_l = rawGyroZ / gyro_scale

                temperature_l = (rawTemp / 340.0) + 36.53

                dt = time.time()
                if debug:
                    print(dt)
                    print("The first IMU's data: {0}, {1}, {2}, {3}, {4}, {5}, {6}".format(accX_l, accY_l, accZ_l, gyroX_l, gyroY_l, gyroZ_l, temperature_l))
            
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
                accX_r = rawAccX / accel_scale
                accY_r = rawAccY / accel_scale
                accZ_r = rawAccZ / accel_scale

                gyro_scale = 65.5 # MPU6050_RANGE_500_DEG
                gyroX_r = rawGyroX / gyro_scale
                gyroY_r = rawGyroY / gyro_scale
                gyroZ_r = rawGyroZ / gyro_scale

                temperature_r = (rawTemp / 340.0) + 36.53
                if debug:
                    print("The second IMU's data: {0}, {1}, {2}, {3}, {4}, {5}, {6}".format(accX_r, accY_r, accZ_r, gyroX_r, gyroY_r, gyroZ_r, temperature_r))
                
                row = [accX_l, accY_l, accZ_l, gyroX_l, gyroY_l, gyroZ_l, temperature_l, accX_r, accY_r, accZ_r, gyroX_r, gyroY_r, gyroZ_r, temperature_r]
                
                imuFile.write("" + str(dt)) 
                for i in row:
                    imuFile.write("," + str(i))
                imuFile.write("\n")


            

