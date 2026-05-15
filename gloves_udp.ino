#include <WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// ======================
// WIFI
// ======================
const char* ssid = "Etisalat 4G iModem-DAAB";
const char* password = "12061884";

// ======================
// UDP
// ======================
WiFiUDP udp;

// 👇 FIXED: YOUR CORRECT PC IP
const char* pcIP = "192.168.0.145";

// 👇 PYTHON PORT
const int pcPort = 5005;

// ======================
// HAND NAME
// ======================
String HAND_NAME = "Right";  // Change to "RIGHT" for right glove

// ======================
// FLEX PINS
// ======================
const int flexPins[5] = {36, 33, 32, 35, 34};

// ======================
void setup() {

  Serial.begin(115200);

  Wire.begin(21, 22);

  mpu.initialize();

  Serial.print("Connecting WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");

  Serial.print("ESP32 IP: ");

  Serial.println(WiFi.localIP());
  
  Serial.print("Sending to PC IP: ");
  
  Serial.println(pcIP);
}

// ======================
void loop() {

  int16_t ax, ay, az, gx, gy, gz;

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  int flex[5];

  for (int i = 0; i < 5; i++) {

    flex[i] = analogRead(flexPins[i]);
  }

  // ======================
  // BUILD MESSAGE
  // ======================
  String msg = "";

  msg += HAND_NAME;
  msg += ",";

  for (int i = 0; i < 5; i++) {

    msg += String(flex[i]);
    msg += ",";
  }

  msg += String(ax);
  msg += ",";

  msg += String(ay);
  msg += ",";

  msg += String(az);
  msg += ",";

  msg += String(gx);
  msg += ",";

  msg += String(gy);
  msg += ",";

  msg += String(gz);

  // ======================
  // SEND UDP
  // ======================
  udp.beginPacket(pcIP, pcPort);

  udp.print(msg);

  udp.endPacket();

  Serial.println(msg);

  delay(50);
}