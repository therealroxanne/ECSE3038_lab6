#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <iostream>
#include <cstdlib> // required for rand() and srand()
#include <ctime> // required for time()
#include "env.h"
#define fanpin 22
#define lightpin 23


void setup() {
  pinMode(fanpin, OUTPUT);
  pinMode(lightpin, OUTPUT);
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
  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;
    float temperature=random(21.0,33.0);
    http.begin(endpoint);
    http.addHeader("Content-type", "application/json");

    StaticJsonDocument<128> doc;
    String httpRequestData;

    doc["Temperature"] = temperature;

    serializeJson(doc, httpRequestData);
    int httpResponseCode=http.PUT(httpRequestData);
    String http_response;
      if(httpResponseCode>0)
    {
      Serial.print("HTTP Response Code: ");
      Serial.println(httpResponseCode);
      Serial.print("Response from server");
      http_response=http.getString();
      Serial.println(http_response);

    }
    else{
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }

      // Free resources
      http.end();
      // Stream& input;

// Stream& input;
http.begin(endpoint);
  
    int httpResponseCode = http.GET();

    if (httpResponseCode>0) 
    {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);

        Serial.print("Response from server: ");
        http_response = http.getString();
        Serial.println(http_response);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
StaticJsonDocument<192> doc;

DeserializationError error = deserializeJson(doc, http_response);

if (error) {
  Serial.print("deserializeJson() failed: ");
  Serial.println(error.c_str());
  return;
}

const char* id = doc["_id"]; // "640e1fc87a0bf6493917690b"
const char* fan_state = doc["fan_state"]; // "True"
const char* light_state = doc["light_state"]; // "False"

if(fanpin==false)
{
  digitalWrite(fanpin, LOW);
}
else
{
  digitalWrite(fanpin, HIGH);
}
if(lightpin==false)
{
  digitalWrite(lightpin, LOW);
}
else
{
  digitalWrite(lightpin, HIGH);
}
  }
  else{
    return;
  }
}
