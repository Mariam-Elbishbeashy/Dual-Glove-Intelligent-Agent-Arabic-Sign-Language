#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

const int flexPins[5] = {36, 33, 32, 35, 34};

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(21, 22);
  mpu.initialize();

  Serial.println("ESP32 READY");
}

void loop() {

  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  int flex[5];
  for (int i = 0; i < 5; i++) {
    flex[i] = analogRead(flexPins[i]);
  }

  // 👇 ADD THIS
  Serial.print("LEFT,");

  for (int i = 0; i < 5; i++) {
    Serial.print(flex[i]);
    Serial.print(",");
  }

  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.print(az); Serial.print(",");
  Serial.print(gx); Serial.print(",");
  Serial.print(gy); Serial.print(",");
  Serial.println(gz);

  delay(50);
}