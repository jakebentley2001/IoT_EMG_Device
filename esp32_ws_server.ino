#include <WiFi.h>
#include <WebServer.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

// SSID and password of Wifi connection:
const char* ssid = "SpectrumSetup-BA";
const char* password = "quickacre283";

WebServer server(80);
WebSocketsServer webSocket = WebSocketsServer(81);

String webpage = "<!DOCTYPE html><html><head><title>Page Title</title></head><body style='background-color: #EEEEEE;'><span style='color: #003366;'><h1>Random number generator</h1><p>The 1st random number is: <span id='rand1'>-</span></p><p>The 2nd random number is: <span id='rand2'>-</span></p><p><button type='button' id='BTN_SEND_BACK'> Send info to ESP32</button></p></span></body><script> var Socket; document.getElementById('BTN_SEND_BACK').addEventListener('click', button_send_back); function init() { Socket = new WebSocket('ws://' + window.location.hostname + ':81/'); Socket.onmessage = function(event) { processCommand(event); }; } function button_send_back(){ var guitar = { brand: 'Gibson', type: 'Dont care', year: 2022, color: 'white', }; Socket.send(JSON.stringify(guitar)) } function processCommand(event) { var obj = JSON.parse(event.data); document.getElementById('rand1').innerHTML = obj.rand1; document.getElementById('rand2').innerHTML = obj.rand1; console.log(obj.rand1); console.log(obj.rand2); } window.onload = function(event) { init(); }</script></html>";
int interval = 1000;
unsigned long previousMillis = 0;

StaticJsonDocument<200> doc_tx;
StaticJsonDocument<200> doc_rx;

void setup() {
  Serial.begin(115200);                 
 
  WiFi.begin(ssid, password);
  Serial.println("Establishing connection to WiFi with SSID: " + String(ssid));
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.print("Connected to network with IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/",[]() {
    server.send(200, "text\html", webpage);
  });
  server.begin();

  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
}
 
void loop() {
  server.handleClient();

  webSocket.loop();



  unsigned long now = millis();
  if (now-previousMillis > interval) {
    String jsonString = "";
    JsonObject object = doc_tx.to<JsonObject>();
    object["rand1"] = random(100);
    object["rand2"] = random(100);

    serializeJson(doc_tx, jsonString);
    Serial.print(jsonString);

    webSocket.broadcastTXT(jsonString);

    previousMillis = now;
  }
}

void webSocketEvent(byte num, WStype_t type, uint8_t * payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("Client Disconnected");
      break;
    case WStype_CONNECTED:
      Serial.println("Client Connected");

      break;
    case WStype_TEXT:
      DeserializationError error = deserializeJson(doc_rx, payload);
      if(error) {
        Serial.print("deserializeJson() failed");
      }
      else {
        const char* g_brand = doc_rx["brand"];
        const char* g_type = doc_rx["type"];
        const int g_year = doc_rx["year"];
        const char* g_color = doc_rx["color"];
        Serial.println("Received guitar info!");
        Serial.println("Brand" + String(g_brand));
        Serial.println("Type" + String(g_type));
        Serial.println("Year" + String(g_year));
        Serial.println("Color" + String(g_color));
      }
      break;
  }
}