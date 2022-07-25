import os
from threading import Thread, Event
import pyaudio
import wave
import time
import argparse
import tkinter as tk
from tkinter.ttk import *

import serial
import re
import time
from threading import Thread

debug = True

parser = argparse.ArgumentParser()
parser.add_argument('--input_device_id', type=int, default=0)
parser.add_argument('--save_dir', type=str, default='../logs/')
parser.add_argument('--imu_port', type=str, default='/dev/cu.usbmodem113201')

args = parser.parse_args()

def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)

class Config:
    def __init__(self):
        # Recording config
        self.frame_rate = 48000
        self.sample_width = 2
        self.n_channels = 6 #CHANGE HERE
        self.total_channels = 6
        self.chunk_size = 4096
        
        self.input_device_id = [args.input_device_id] # For H6 device. Please use the get_microphone_device_id to get 
        self.start_rec = False
        self.audiofilename = ""
        self.imufilename = ""
        self.audiofile = None
        self.imufile = None

        self.close_imu = False

        self.sensors_dps_to_rads = 0.017453293
        self.sensors_gravity_standard = 9.80665

        # serial port open procedure

        self.ser = serial.Serial()
        self.ser.port = args.imu_port #Arduino serial port, should change accrodingly
        self.ser.baudrate = 115200
        self.ser.timeout = 10 
        self.ser.open()


def mainloop(config):
    root = tk.Tk()
    root.title("Recording...")
   
    tk.Label(root, text="Device: ").grid(row=0)
    tk.Label(root, text="SampleWidth:").grid(row=1)
    tk.Label(root, text="Channels: ").grid(row=2)
    entry1 = tk.Entry(root)
    entry2 = tk.Entry(root)
    entry3 = tk.Entry(root)

    entry1.insert(10, "Zoom H6")
    entry1.grid(row=0, column=1)
    entry1.config(state='readonly')
    entry2.insert(10, "2")
    entry2.grid(row=1, column=1)
    entry2.config(state='readonly')
    entry3.insert(10, "6")
    entry3.grid(row=2, column=1)
    entry3.config(state='readonly')

    tk.Button(root, text='Start', command=lambda: start_recv(config)).grid(row=3, column=0, sticky=tk.W, pady=10)
    tk.Button(root, text='Stop', command=lambda: stop_recv(config)).grid(row=3, column=1, sticky=tk.W, pady=10)
    
    root.mainloop()

def start_recv(config):
    if config.ser.is_open==True:
        print("Start Recording...")
        config.start_rec = True
    else:
        print("Serial open failed, Please check the Serial Config")

def stop_recv(config):
    config.start_rec = False

# pushing the audio data to audio file.
def stream_callback(config, audiofile):
    def callback(in_data, frame_count, time_info, status):
        # data = np.frombuffer(in_data, dtype=np.int16)
        if(config.start_rec):
            audiofile.writeframes(in_data)
         
        return (None, pyaudio.paContinue)
    return callback

def imu_callback(config):
    with open(config.imufilename, 'a') as imuFile:
        while True:
            if config.close_imu:
                break

            if config.start_rec:
                line=config.ser.readline()
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

                    accX_l *= config.sensors_gravity_standard
                    accY_l *= config.sensors_gravity_standard
                    accZ_l *= config.sensors_gravity_standard

                    gyro_scale = 65.5 # MPU6050_RANGE_500_DEG
                    gyroX_l = rawGyroX / gyro_scale
                    gyroY_l = rawGyroY / gyro_scale
                    gyroZ_l = rawGyroZ / gyro_scale

                    gyroX_l *= config.sensors_dps_to_rads
                    gyroY_l *= config.sensors_dps_to_rads
                    gyroZ_l *= config.sensors_dps_to_rads

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

                    accX_r *= config.sensors_gravity_standard
                    accY_r *= config.sensors_gravity_standard
                    accZ_r *= config.sensors_gravity_standard

                    gyro_scale = 65.5 # MPU6050_RANGE_500_DEG
                    gyroX_r = rawGyroX / gyro_scale
                    gyroY_r = rawGyroY / gyro_scale
                    gyroZ_r = rawGyroZ / gyro_scale

                    gyroX_r *= config.sensors_dps_to_rads
                    gyroY_r *= config.sensors_dps_to_rads
                    gyroZ_r *= config.sensors_dps_to_rads

                    temperature_r = (rawTemp / 340.0) + 36.53
                    if debug:
                        print("The second IMU's data: {0}, {1}, {2}, {3}, {4}, {5}, {6}".format(accX_r, accY_r, accZ_r, gyroX_r, gyroY_r, gyroZ_r, temperature_r))
                    
                    row = [accX_l, accY_l, accZ_l, gyroX_l, gyroY_l, gyroZ_l, temperature_l, accX_r, accY_r, accZ_r, gyroX_r, gyroY_r, gyroZ_r, temperature_r]
                    
                    imuFile.write("" + str(dt)) 
                    for i in row:
                        imuFile.write("," + str(i))
                    imuFile.write("\n")

def recv_multi_track(config):
    p = pyaudio.PyAudio()
    
    audiofile = wave.open(config.audiofilename, "wb")
    audiofile.setnchannels(config.n_channels)
    # sampling rate of audio
    audiofile.setframerate(config.frame_rate)
    # sampling deepth
    audiofile.setsampwidth(config.sample_width)

    stream = p.open(format=p.get_format_from_width(config.sample_width),
                    channels=config.n_channels,
                    rate=config.frame_rate,
                    input=True, 
                    input_device_index=config.input_device_id[0],
                    frames_per_buffer=config.chunk_size,
                    stream_callback=stream_callback(config, audiofile))

        # threads for processing data
        #Thread(target=process_data, args=(config), daemon=True).start()
    
    return [stream], p

# used to test whether this is the H6 device. 
def get_microphone_device_id():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
            print("Max input channels:", p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels'))

if __name__ == '__main__':
    
    config = Config()
    get_microphone_device_id()

    if not os.path.exists(args.save_dir):
        os.mkdir(args.save_dir)
    # if (not os.path.exists("../logs/")):
    #     os.mkdir("../logs/")

    now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
    config.audiofilename = args.save_dir+now+r"_recording.wav"
    config.imufilename = args.save_dir+now+r"_imu.txt"

    with open(config.imufilename, 'w') as imuFile:
        imuFile.write("timestamp" + "," + "accX_l" + "," + "accY_l" + "," + "accZ_l" + "," + "gyroX_l"+ "," + "gyroY_l" + "," + "gyroZ_l"  + "," + "temp_l" + "," + "accX_r" + "," + "accY_r" + "," + "accZ_r" + "," + "gyroX_r"+ "," + "gyroY_r" + "," + "gyroZ_r"  + "," + "temp_r" + "\n")

    task_imu = Thread(target=imu_callback, args=(config,))
    task_imu.start()

    stream_list, p = recv_multi_track(config)
    mainloop(config)

    config.close_imu = True
    task_imu.join()

    #close
    for stream_item in stream_list:
        stream_item.stop_stream()
        stream_item.close()

    p.terminate()
