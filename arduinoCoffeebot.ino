#include <SoftwareSerial.h>
#include <SparkFunESP8266WiFi.h>
enum State { IDLING, BREWING };
const int TEMPERATURE_SIZE = 40;
const int SLOPE_SIZE = 10;
//////////////////////////////
// WiFi Network Definitions //
//////////////////////////////
// Replace these two character strings with the name and
// password of your WiFi network.

// Your network and password
const char mySSID[] = "NETWORK";
const char myPSK[] = "PASSWORD";

// Insert your keys here
const String host = "HOST";
const String url = "/add_coffee";
State current;
int degreesF;
float temperatureReadings[TEMPERATURE_SIZE];
float temperatureSlopes[SLOPE_SIZE];
void setup() {
  int status;
  Serial.begin(9600);
  current = IDLING;
  initReadings();

  delay(1000);

  status = esp8266.begin();
  while (status <= 0)
  {
    Serial.println(F("Unable to communicate with shield. Looping"));
    status = esp8266.begin();
    delay(1000);
  }

  esp8266.setMode(ESP8266_MODE_STA); // Set WiFi mode to station
  if (esp8266.status() <= 0) // If we're not already connected
  {
    while(esp8266.connect(mySSID, myPSK) < 0)
    {
      Serial.println(F("Error connecting"));
      delay(1000);
    }
  }
}

void loop() {
  switch (current) {
    case IDLING:
      degreesF = getDegreesF();
      addTemperature();
      addTemperatureSlope();
      if (getSlopesAverage() < -.45) {
        current = BREWING;
      }
      break;
    case BREWING:
      delay(210000);
      postToSlack();
      current = IDLING;
      initReadings();
      break;
  }

  delay(1000);
}

void initReadings() {
  for(int i = 0; i < TEMPERATURE_SIZE; i++) {
    temperatureReadings[i] = 0.0;
  }
}

int getDegreesF() {
  const int temperaturePin = 0;
  float voltage, degreesC, degreesF;

  voltage = getVoltage(temperaturePin);

  // Per the TMP36 datasheet
  degreesC = (voltage - 0.5) * 100.0;

  degreesF = degreesC * (9.0/5.0) + 32.0;
  return degreesF;
}

float getVoltage(int pin) {
  return (analogRead(pin) * 0.004882814);
}

void addTemperature() {
  for(int i = TEMPERATURE_SIZE - 1; i > 0; i--) {
    temperatureReadings[i] = temperatureReadings[i - 1];
  }
  temperatureReadings[0] = degreesF;
}

void addTemperatureSlope() {
  for(int i = SLOPE_SIZE - 1; i > 0; i--) {
    temperatureSlopes[i] = temperatureSlopes[i - 1];
  }
  temperatureSlopes[0] = (temperatureReadings[0] - temperatureReadings[TEMPERATURE_SIZE - 1]) / TEMPERATURE_SIZE;
}

float getSlopesAverage() {
  float slopesSum = 0.0;
  for(int i = 0; i < SLOPE_SIZE; i++) {
    slopesSum = slopesSum + temperatureSlopes[i];
  }
  float avg = slopesSum / SLOPE_SIZE;
  return avg;
}

void postToSlack() {
  
  // Create a client, and initiate a connection
  ESP8266Client client;
  // if the client connects, make the api call
  if (client.connect(host, 80)) {
    // the API request
    String PostData="text=Fresh pot of coffee!&temperature=" + String(degreesF);
    client.print("POST ");
    client.print(url);
    client.println(" HTTP/1.1");
    client.print("Host: ");
    client.println(host);
    client.println("User-Agent: ArduinoIoT/1.0");
    client.println("Content-Type: application/x-www-form-urlencoded;");
    client.print("Content-Length: ");
    client.println(PostData.length());
    client.println();
    client.println(PostData);
  
    delay(100);
    
    // printing out the results from the API call
    while (client.available()) // While there's data available
        Serial.write(client.read()); // Read it and print to serial

    // Disconnect if the connection wasn't already closed
    if (client.connected()) {
      client.stop();
    }

  } else {
    Serial.println("didn't connect to port");
  }
}
