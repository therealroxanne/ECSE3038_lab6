#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "env.h"



void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
	
	// WiFi_SSID and WIFI_PASS should be stored in the env.h
  WiFi.begin(WIFI_USER, WIFI_PASS);

	// Connect to wifi
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // put your main code here, to run repeatedly:
}