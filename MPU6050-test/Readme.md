## Raw Data -> Real Data

#### For Acc

1. Scaling

   ```c
   float accel_scale = 1;
   if (accel_range == MPU6050_RANGE_16_G)
     accel_scale = 2048;
   if (accel_range == MPU6050_RANGE_8_G)
     accel_scale = 4096;
   if (accel_range == MPU6050_RANGE_4_G)
     accel_scale = 8192;
   if (accel_range == MPU6050_RANGE_2_G)
     accel_scale = 16384;
   
   // setup range dependant scaling
   accX = ((float)rawAccX) / accel_scale;
   accY = ((float)rawAccY) / accel_scale;
   accZ = ((float)rawAccZ) / accel_scale;
   ```

1. Standardize

   ```c
   accX *= SENSORS_GRAVITY_STANDARD;
   accY *= SENSORS_GRAVITY_STANDARD;
   accZ *= SENSORS_GRAVITY_STANDARD;
   
   //SENSORS_GRAVITY_STANDARD = 9.80665F;
   ```

#### For Gyro

1. Scaling

   ```c
   float gyro_scale = 1;
   if (gyro_range == MPU6050_RANGE_250_DEG)
     gyro_scale = 131;
   if (gyro_range == MPU6050_RANGE_500_DEG)
     gyro_scale = 65.5;
   if (gyro_range == MPU6050_RANGE_1000_DEG)
     gyro_scale = 32.8;
   if (gyro_range == MPU6050_RANGE_2000_DEG)
     gyro_scale = 16.4;
   
   gyroX = ((float)rawGyroX) / gyro_scale;
   gyroY = ((float)rawGyroY) / gyro_scale;
   gyroZ = ((float)rawGyroZ) / gyro_scale;
   ```

2. Standardize

   ```c
   gyroX *= SENSORS_DPS_TO_RADS;
   gyroY *= SENSORS_DPS_TO_RADS;
   gyroZ *= SENSORS_DPS_TO_RADS;
   
   //SENSORS_DPS_TO_RADS = 0.017453293F;
   ```

   

