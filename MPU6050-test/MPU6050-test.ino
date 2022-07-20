// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu_l;
Adafruit_MPU6050 mpu_r;

<<<<<<< HEAD
uint8_t data_l[14];
uint8_t data_r[14];

String hexStr;
char hexNum[2];

void errorBlk(void) {
  digitalWrite(LED_BUILTIN, HIGH);   
  delay(500);                       
  digitalWrite(LED_BUILTIN, LOW);    
  delay(500);   
  digitalWrite(LED_BUILTIN, HIGH);   
  delay(500);                       
  digitalWrite(LED_BUILTIN, LOW);    
  delay(2000);    
  
}
=======
>>>>>>> 317d7d8278d963dfe54e9445dfd1de083c1f4c61

void setup(void) {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  // Try to initialize!
<<<<<<< HEAD
  if (!mpu_l.begin(0X69)) {
    Serial.println("Failed to find the left MPU6050 chip");
=======
  if (!mpu_l.begin(0x69)) {
    Serial.println("Failed to find MPU6050 chip");
>>>>>>> 317d7d8278d963dfe54e9445dfd1de083c1f4c61
    while (1) {
      delay(10);
      errorBlk();
    }
  }
<<<<<<< HEAD
  
  if (!mpu_r.begin()) {
    Serial.println("Failed to find the right MPU6050 chip");
    while (1) {
      delay(10); 
      errorBlk();                  
    }
  }
  
  //four config param: MPU6050_RANGE_2_G, MPU6050_RANGE_4_G, MPU6050_RANGE_8_G, MPU6050_RANGE_16_G
  mpu_l.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu_r.setAccelerometerRange(MPU6050_RANGE_4_G);
  delay(100);
=======
  Serial.println("MPU6050 Found!");

  if (!mpu_r.begin(0x68)) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu_l.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu_r.setAccelerometerRange(MPU6050_RANGE_4_G);
  
  // Serial.print("Accelerometer range set to: ");
  // switch (mpu.getAccelerometerRange()) {
  // case MPU6050_RANGE_2_G:
  //   Serial.println("+-2G");
  //   break;
  // case MPU6050_RANGE_4_G:
  //   Serial.println("+-4G");
  //   break;
  // case MPU6050_RANGE_8_G:
  //   Serial.println("+-8G");
  //   break;
  // case MPU6050_RANGE_16_G:
  //   Serial.println("+-16G");
  //   break;
  // }
  mpu_l.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu_r.setGyroRange(MPU6050_RANGE_500_DEG);

  // Serial.print("Gyro range set to: ");
  // switch (mpu.getGyroRange()) {
  // case MPU6050_RANGE_250_DEG:
  //   Serial.println("+- 250 deg/s");
  //   break;
  // case MPU6050_RANGE_500_DEG:
  //   Serial.println("+- 500 deg/s");
  //   break;
  // case MPU6050_RANGE_1000_DEG:
  //   Serial.println("+- 1000 deg/s");
  //   break;
  // case MPU6050_RANGE_2000_DEG:
  //   Serial.println("+- 2000 deg/s");
  //   break;
  // }

  mpu_l.setFilterBandwidth(MPU6050_BAND_260_HZ);
  mpu_r.setFilterBandwidth(MPU6050_BAND_260_HZ);

  // Serial.print("Filter bandwidth set to: ");
  // switch (mpu.getFilterBandwidth()) {
  // case MPU6050_BAND_260_HZ:
  //   Serial.println("260 Hz");
  //   break;
  // case MPU6050_BAND_184_HZ:
  //   Serial.println("184 Hz");
  //   break;
  // case MPU6050_BAND_94_HZ:
  //   Serial.println("94 Hz");
  //   break;
  // case MPU6050_BAND_44_HZ:
  //   Serial.println("44 Hz");
  //   break;
  // case MPU6050_BAND_21_HZ:
  //   Serial.println("21 Hz");
  //   break;
  // case MPU6050_BAND_10_HZ:
  //   Serial.println("10 Hz");
  //   break;
  // case MPU6050_BAND_5_HZ:
  //   Serial.println("5 Hz");
  //   break;
  // }
>>>>>>> 317d7d8278d963dfe54e9445dfd1de083c1f4c61

  //four config param: MPU6050_RANGE_250_DEG, MPU6050_RANGE_500_DEG, MPU6050_RANGE_1000_DEG, MPU6050_RANGE_2000_DEG
  mpu_l.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu_r.setGyroRange(MPU6050_RANGE_500_DEG);
  delay(100);
  digitalWrite(LED_BUILTIN, HIGH); 
}

void loop() {
  hexStr = "";
  mpu_l.getRawDataBytes(data_l);
  mpu_r.getRawDataBytes(data_r);

<<<<<<< HEAD
  for(int i = 0; i < sizeof(data_l); i++){
    sprintf(hexNum, "%02X", data_l[i]);
    hexStr =  hexStr + hexNum;
  }
  
  for(int i = 0; i < sizeof(data_r); i++){
    sprintf(hexNum, "%02X", data_r[i]);
    hexStr =  hexStr + hexNum;
  }
  Serial.println(hexStr);
  
//  Serial.print(data_l);
//  Serial.print(',');
//  Serial.println(data_r);
//  
//  /* Get new sensor events with the readings */
//  sensors_event_t a_l, g_l, temp_l;
//  sensors_event_t a_r, g_r, temp_r;
//  mpu_l.getEvent(&a_l, &g_l, &temp_l);
//  mpu_r.getEvent(&a_r, &g_r, &temp_r);
//  
//  /* Print out the values */
////  Serial.print("Acceleration X: ");
//  Serial.print(a_l.acceleration.x);
//  Serial.print(",");
//  Serial.print(a_l.acceleration.y);
//  Serial.print(",");
//  Serial.print(a_l.acceleration.z);
//  Serial.print(",");
//
//  Serial.print(g_l.gyro.x);
//  Serial.print(",");
//  Serial.print(g_l.gyro.y);
//  Serial.print(",");
//  Serial.print(g_l.gyro.z);
//  Serial.print(",");
//  
//  Serial.print(a_r.acceleration.x);
//  Serial.print(",");
//  Serial.print(a_r.acceleration.y);
//  Serial.print(",");
//  Serial.print(a_r.acceleration.z);
//  Serial.print(",");
//
//  Serial.print(g_r.gyro.x);
//  Serial.print(",");
//  Serial.print(g_r.gyro.y);
//  Serial.print(",");
//  Serial.print(g_r.gyro.z);
////  Serial.print(",");
////  Serial.print(temp_r.temperature);
//
//  Serial.println("");
=======
  /* Get new sensor events with the readings */
  // sensors_event_t a, g, temp;
  // mpu.getEvent(&a, &g, &temp);
  uint16_t buffer_l[6];
  uint16_t buffer_r[6];

  mpu_l.getEventRaw(buffer_l);
  mpu_r.getEventRaw(buffer_r);

  //L ACC RAW
  Serial.print(buffer_l[0]);
  Serial.print(',');
  Serial.print(buffer_l[1]);
  Serial.print(',');
  Serial.print(buffer_l[2]);
  Serial.print(',');

  //L GYR RAW
  Serial.print(buffer_l[3]);
  Serial.print(',');
  Serial.print(buffer_l[4]);
  Serial.print(',');
  Serial.print(buffer_l[5]);
  Serial.print(',');

  //R ACC RAW
  Serial.print(buffer_r[0]);
  Serial.print(',');
  Serial.print(buffer_r[1]);
  Serial.print(',');
  Serial.print(buffer_r[2]);
  Serial.print(',');

  //R GYR RAW
  Serial.print(buffer_r[3]);
  Serial.print(',');
  Serial.print(buffer_r[4]);
  Serial.print(',');
  Serial.print(buffer_r[5]);

  Serial.println("");

  /* Print out the values */
//  Serial.print("Acceleration X: ");
  // Serial.print(a.acceleration.x);
  // Serial.print(",");
  // Serial.print(a.acceleration.y);
  // Serial.print(",");
  // Serial.print(a.acceleration.z);
  // Serial.print(",");
//  Serial.println(" m/s^2");

//  Serial.print("Rotation X: ");
  // Serial.print(g.gyro.x);
  // Serial.print(",");
//  Serial.print(", Y: ");
  // Serial.print(g.gyro.y);
  // Serial.print(",");
//  Serial.print(", Z: ");
  // Serial.print(g.gyro.z);
//  Serial.println(" rad/s");

//  Serial.print("Temperature: ");
//  Serial.print(temp.temperature);
//  Serial.println(" degC");

>>>>>>> 317d7d8278d963dfe54e9445dfd1de083c1f4c61
}
