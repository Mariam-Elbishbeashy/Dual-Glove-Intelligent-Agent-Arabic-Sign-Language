#include <WiFi.h>
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

const char* ssid = "Etisalat 4G iModem-96DB";
const char* password = "13804518";

WiFiServer server(80);

// Change this on each ESP32
String HAND_NAME = "LEFT";   // LEFT or RIGHT

const int flexPins[5] = {36, 33, 32, 35, 34};

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(21, 22);
  mpu.initialize();

  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Client connected");

    while (client.connected()) {
      int16_t ax, ay, az, gx, gy, gz;
      mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

      int flexValues[5];
      for (int i = 0; i < 5; i++) {
        flexValues[i] = analogRead(flexPins[i]);
      }

      client.print(HAND_NAME);
      client.print(",");

      for (int i = 0; i < 5; i++) {
        client.print(flexValues[i]);
        client.print(",");
      }

      client.print(ax); client.print(",");
      client.print(ay); client.print(",");
      client.print(az); client.print(",");

      client.print(gx); client.print(",");
      client.print(gy); client.print(",");
      client.println(gz);

      delay(200);
    }

    client.stop();
    Serial.println("Client disconnected");
  }
}