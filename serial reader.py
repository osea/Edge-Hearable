#注意串口占用问题。使用Due的programming port和serial reader使用的是同一串口

import time
import serial
from datetime import datetime

ser = serial.Serial(
  port='COM10',#串口，与Arduino IDE中连接的串口保持一致
  baudrate=115200,#波特率，与Arduino代码保持一致
  parity=serial.PARITY_ODD,
  stopbits=serial.STOPBITS_TWO,
  bytesize=serial.SEVENBITS
)

data = ''

#注：在串口答应时最好全部采用统一数据格式，如在开头打印“MPU test”会导致之后打印imu 6轴数据时掉数据或乱码
while True:
  with open('C:\\Users\\zhang\\Desktop\\INFO.txt', 'a') as f: #根据情况修改
    data = ser.readline()
    f.writelines(data.decode())
    print(datetime.now(), data)#testing the sampling frequency