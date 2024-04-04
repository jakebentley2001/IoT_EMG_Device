#include <Arduino.h>

#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClientSecure.h>

#include <ArduinoJson.h>

#include <WebSocketsClient.h>
#include <SocketIOclient.h>


const char* ssid = "SpectrumSetup-BA";
const char* password = "quickacre283";
const char* webSocketServerAddress = "192.168.1.29";
const int webSocketServerPort = 5000; // Port of your WebSocket server

WebSocketsClient webSocket;
SocketIOclient socketIO;

bool sendDataFlag = false;

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi
  Serial.println("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to WebSocket server
  Serial.println("Connecting to WebSocket server");
  delay(1000);
  socketIO.begin(webSocketServerAddress, webSocketServerPort);
  socketIO.onEvent(socketIOEvent);
}

void loop() {
  socketIO.loop();
  
  // Send the number directly to the server
  socketIO.sendEVENT("123"); // Replace "123" with your desired number
  
  delay(2000); // Delay for 2 seconds before sending again
}

void socketIOEvent(socketIOmessageType_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case sIOtype_DISCONNECT:
      Serial.printf(".");
      break;
    case sIOtype_CONNECT:
      Serial.printf("*", payload);

      // Join default namespace (no auto join in Socket.IO V3)
      socketIO.send(sIOtype_CONNECT, "/");
      break;
    case sIOtype_EVENT:
      Serial.printf("[IOc] get event: %.*s\n", length, payload);
      break;
    case sIOtype_ACK:
      Serial.printf("[IOc] get ack: %u\n", length);
      break;
    case sIOtype_ERROR:
      Serial.printf("[IOc] get error: %u\n", length);
      break;
    case sIOtype_BINARY_EVENT:
      Serial.printf("[IOc] get binary: %u\n", length);
      break;
    case sIOtype_BINARY_ACK:
      Serial.printf("[IOc] get binary ack: %u\n", length);
      break;
  }
}