#include <ArduinoBLE.h>

// Define the BLE Service and Characteristic
BLEService customService("19B10000-E8F2-537E-4F6C-D104768A1214"); // Define a custom service UUID
BLEFloatCharacteristic dataCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify); // Define a custom characteristic UUID

const int ledPin = 12; // Use the built-in LED
const int buttonPin = 4;
int buttonState = 0;
unsigned long buttonPressStartTime = 0;
const unsigned long debounceTime = 500; 

void setup() {
  Serial.begin(9600);    // Initialize serial communication
  //while (!Serial);

  pinMode(ledPin, OUTPUT); // Set the LED pin as an output
  digitalWrite(ledPin, LOW); // Turn off the LED

  pinMode(buttonPin, INPUT);

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("ContinuousData"); // Set the local name advertised by the BLE peripheral
  BLE.setAdvertisedService(customService); // Advertise the service
  customService.addCharacteristic(dataCharacteristic); // Add the characteristic to the service
  BLE.addService(customService); // Add the service
  dataCharacteristic.setValue(0); // Initialize the characteristic value

  BLE.advertise(); // Start advertising
  Serial.println("BLE Peripheral device started, waiting for connections...");
}


//void loop() {
  // read the state of the pushbutton value:
 // buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
 // if (buttonState == HIGH) {
    // turn LED on:
 //   connectAndSendData();
 // } else {
  //  digitalWrite(ledPin, LOW);
    // turn LED off:
    
//  }
//}

void loop() {
  // Read the state of the pushbutton
  int newButtonState = digitalRead(buttonPin);

  // If the button state has changed
  if (newButtonState != buttonState) {
    // Record the current time
    buttonPressStartTime = millis();
    // Update the button state
    buttonState = newButtonState;
  }

  // If the button has been in the HIGH state for at least debounceTime milliseconds
  if (buttonState == HIGH && (millis() - buttonPressStartTime >= debounceTime)) {
    connectAndSendData();
  }
}



void connectAndSendData() {
  digitalWrite(ledPin, HIGH); // Turn on the LED

  // Blink LED while waiting for a BLE central to connect
  while (!BLE.central()) {
    digitalWrite(ledPin, HIGH); // Turn LED on
    delay(500); // Wait 500 milliseconds
    digitalWrite(ledPin, LOW); // Turn LED off
    delay(500); // Wait 500 milliseconds
  }

  BLEDevice central = BLE.central(); // Wait for a central to connect

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    digitalWrite(ledPin, HIGH);

    while (central.connected()) {
      float sensorValue = analogRead(A1) * (3.3 / 1023.0); // Read a sensor value (replace with your actual data source)
      dataCharacteristic.writeValue(sensorValue); // Update the characteristic value with the sensor data
      delay(50); // Delay between updates
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }

  digitalWrite(ledPin, LOW); // Turn off the LED
}