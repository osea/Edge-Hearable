# Edge-Hearable
Open-sourced edge compputing hearable platform from Pervasive Interaction Lab of Tsinghua University.

## Install

1. Install the "Scheduler" library to your Arduino IDE.
2. Get the "Arduino Due" in the board management tool. 
3. Install the "Adafruit MPU6050" library to your Arduino IDE.



## DataLogger

1. Connect Zoom H6 and Arduino Mega 2560 to the PC.

2. Check the port of Arduino Mega 2560 -> Change Config.ser.port. (using --imu_port on command)

3. Run datalogger.py -> Get Zoom H6 device ID -> Change Config.input_device_id. (using --input_device_id on command)

4. Run datalogger.py -> Get the TK UI to freely start and stop your recording. (Don't forget to set save directory using --save_dir on command)

5. Example: python datalogger.py --save_dir ../logs1/ --input_device_id 2 --imu_port COM5

   

## Bi-Toolkit(WINDOWS 10 ONLY)

1. Connect two (ZOOM-H6 + Arduino Mega 2560) successively, Find the Arduino port and H6 device pairs.
2. Create two cmd, Using --input_device_id and --imu_port and --save_dir to seperate two toolkit.

