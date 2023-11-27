#include <TinyGPS++.h>
#include <SoftwareSerial.h>

const int rxPin = D2;
const int txPin = D1;

TinyGPSPlus gps;
SoftwareSerial ss(rxPin, txPin);

void setup() {
  Serial.begin(9600); // Inisialisasi komunikasi serial dengan baud rate 9600
  ss.begin(9600); // Inisialisasi komunikasi serial dengan GPS

  Serial.println("Mengambil Titik Koordinat GPS...");
}
 
void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "GET_COORDINATE") {
      String coordinate = "-8.159085,113.721818";
      Serial.println(String(coordinate));
    }
  }
}
