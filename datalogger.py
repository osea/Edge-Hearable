import os
from threading import Thread, Event
import numpy as np
import pyaudio
import wave
import time
import tkinter as tk
from tkinter.ttk import *

class Config:
    def __init__(self):
        # Recording config
        self.frame_rate = 48000
        self.sample_width = 2
        self.n_channels = 6 #CHANGE HERE
        self.total_channels = 6
        self.chunk_size = 4096
        
        self.input_device_id = [1] # For H6 device. Please use the get_microphone_device_id to get 
        self.start_rec = False
        self.audiofilename = ""
        self.imufilename = ""
        self.audiofile = None
        self.imufile = None

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
    tk.Button(root, text = 'Stop', command=lambda: stop_recv(config)).grid(row=3, column=1, sticky=tk.W, pady=10)
    
    root.mainloop()

def start_recv(config):
    print("Start Recording...")
    config.start_rec = True

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

def recv_multi_track(config):
    p = pyaudio.PyAudio()
    
    audiofile = wave.open(config.audiofilename, "wb")
    audiofile.setnchannels(config.n_channels)
    audiofile.setframerate(config.frame_rate)
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

if __name__ == '__main__':
    
    config = Config()
    get_microphone_device_id()

    now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
    config.audiofilename = "./logs/"+now+r"_recording.wav"
    config.imufilename = "./logs/"+now+r"_imu.txt"

    stream_list, p = recv_multi_track(config)
    mainloop(config)

    #close
    for stream_item in stream_list:
        stream_item.stop_stream()
        stream_item.close()

    p.terminate()
