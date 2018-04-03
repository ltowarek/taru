// Board: Generic ESP8266 Module
// Flash Mode: QIO
// Flash Size: 4M (1M SPIFFS)
// Reset Method: nodemcu

#include <DHTesp.h>
#include <ESP8266WiFi.h>
#include <ThingSpeak.h>

const char *ssid = "ssid";
const char *password = "password";
const unsigned int max_retries = 3;
WiFiClient client;

const char *server = "api.thingspeak.com";
const unsigned long channel_id = 0;
const char *write_api_key = "write_api_key";
const char *read_api_key = "read_api_key";

const struct Fields {
  unsigned int temperature = 1;
  unsigned int humidity = 2;
  unsigned int heat_index = 3;
} fields;

typedef unsigned long milliseconds_t;
const milliseconds_t posting_interval = 30L * 1000L;
milliseconds_t last_update_time = 0;

const unsigned int dht_pin = 5;

DHTesp dht;

typedef float celsius_degrees_t;
celsius_degrees_t temperature = 0.0f;
celsius_degrees_t heat_index = 0.0f;

typedef float percent_t;
percent_t humidity = 0.0f;

void setup() {
  Serial.begin(9600);
  Serial.println();
  Serial.println();

  if (!connect_wifi()) {
    Serial.println("Failed to connect to WiFi!");
  }

  dht.setup(dht_pin);
}

bool connect_wifi() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to ");
    Serial.println(ssid);
    for (unsigned int i = 1; i <= max_retries; ++i) {
      Serial.print("Attempt [");
      Serial.print(i);
      Serial.print("/");
      Serial.print(max_retries);
      Serial.println("]");

      WiFi.disconnect();
      WiFi.begin(ssid, password);
      delay(5000);

      if (WiFi.status() == WL_CONNECTED) {
        Serial.println("OK");
        ThingSpeak.begin(client);
        break;
      }
    }
  }
  return WiFi.status() == WL_CONNECTED;
}

void loop() {
  if (!should_post_update()) return;
  last_update_time = millis();

  if (!set_temperature()) {
    Serial.println("Failed to set temperature!");
    return;
  }
  Serial.print("Temperature [C]: ");
  Serial.println(temperature);

  if (!set_humidity()) {
    Serial.println("Failed to set humidity!");
    return;
  }
  Serial.print("Humidity [%]: ");
  Serial.println(humidity);

  if (!set_heat_index()) {
    Serial.println("Failed to set heat index!");
    return;
  }
  Serial.print("Heat Index [C]: ");
  Serial.println(heat_index);

  if (!connect_wifi()) {
    Serial.println("Failed to connect to WiFi!");
    return;
  }

  if (!write_fields()) {
    Serial.println("Failed to write fields to ThingSpeak!");
    return;
  }
}

bool set_temperature() {
  temperature = dht.getTemperature();
  return !dht.getStatus();
}

bool set_humidity() {
  humidity = dht.getHumidity();
  return !dht.getStatus();
}

bool set_heat_index() {
  heat_index = dht.computeHeatIndex(temperature, humidity, false);
  return !dht.getStatus();
}

bool should_post_update() {
  return millis() - last_update_time >= posting_interval;
}

bool write_fields() {
  ThingSpeak.setField(fields.temperature, temperature);
  ThingSpeak.setField(fields.humidity, humidity);
  ThingSpeak.setField(fields.heat_index, heat_index);
  return ThingSpeak.writeFields(channel_id, write_api_key);
}

