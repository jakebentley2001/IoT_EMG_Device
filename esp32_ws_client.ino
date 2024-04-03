#include <WiFi.h>
#include <WebSocketsClient.h>

const char* ssid = "SSID";
const char* password = "PSWD";
const char* webSocketServerAddress = "ws://127.0.0.1:5000";
const int webSocketServerPort = 5000; // Port of your WebSocket server

WebSocketsClient webSocket;
bool sendDataFlag = false;

void setup() {
  Serial.begin(115200);
  delay(100);

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
  webSocket.begin(webSocketServerAddress, webSocketServerPort);
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  webSocket.loop();
  
  // Check if sendDataFlag is true, then send data to server
  if (sendDataFlag) {
    webSocket.sendTXT("Hello from ESP32!");
    sendDataFlag = false; // Reset flag
  }
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("Disconnected from WebSocket server");
      break;
    case WStype_CONNECTED:
      Serial.println("Connected to WebSocket server");
      break;
    case WStype_TEXT:
      Serial.println("Received message from server: " + String((char *)payload));
      // Check if the received message contains a special character
      for (size_t i = 0; i < length; i++) {
        if (payload[i] == '#') { // Change '#' to your special character
          // Set flag to send data back to server
          sendDataFlag = true;
          break;
        }
      }
      break;
    case WStype_BIN:
      Serial.println("Received binary data from server");
      break;
    case WStype_ERROR:
      Serial.println("WebSocket error occurred");
      break;
  }
}
