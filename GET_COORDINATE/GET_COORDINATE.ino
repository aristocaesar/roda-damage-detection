#include <TinyGPS++.h>
#include <SoftwareSerial.h>

const int rxPin = D2;
const int txPin = D1;
const int ledPin = LED_BUILTIN;

TinyGPSPlus gps;
SoftwareSerial ss(rxPin, txPin);

void setup() {
  Serial.begin(9600);
  ss.begin(9600);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void loop() {
  while (ss.available() > 0) {
    char c = ss.read();
    if (c == '\n') {
      getCoordinate();
    } else {
      gps.encode(c);
    }
  }

  if (gps.location.isUpdated()) {
    digitalWrite(ledPin, !digitalRead(ledPin));
  }
}

void getCoordinate() {
  String command = Serial.readStringUntil('\n');

  if (command == "GET_COORDINATE") {
    if (gps.location.isValid()) {
      String coordinates = String(gps.location.lat(), 6) + "," + String(gps.location.lng(), 6);
      Serial.println(coordinates);
    } else {
      Serial.println("GPS data not valid.");
    }
  }
}
