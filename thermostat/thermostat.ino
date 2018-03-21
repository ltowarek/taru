#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <ThingSpeak.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

const char *ssid = "ssid";
const char *password = "password";
const unsigned int max_retries = 3;
WiFiClient client;

const char *server = "api.thingspeak.com";
const unsigned long channel_id = 0;
const char *write_api_key = "write_api_key";
const char *read_api_key = "read_api_key";

const struct Fields {
  unsigned int current_temperature = 1;
  unsigned int heater_state = 2;
  unsigned int requested_temperature = 3;
  unsigned int requested_day_temperature = 4;
  unsigned int requested_night_temperature = 5;
  unsigned int hysteresis = 6;
} fields;

typedef unsigned long milliseconds_t;
const milliseconds_t posting_interval = 15L * 1000L;
milliseconds_t last_update_time = 0;

WiFiUDP ntp_udp;
NTPClient time_client(ntp_udp);

typedef int hours_t;
hours_t night_start = 21;
hours_t night_end = 8;

const unsigned int heater_pin = 13;
const unsigned int one_wire_pin = 12;
const unsigned int led_pin = 2;

OneWire one_wire(one_wire_pin);
DallasTemperature sensors(&one_wire);

bool heater_state = LOW;

typedef float celsius_degrees_t;
celsius_degrees_t current_temperature = 0.0f;
celsius_degrees_t requested_temperature = 0.0f;
celsius_degrees_t requested_day_temperature = 0.0f;
celsius_degrees_t requested_night_temperature = 0.0f;
celsius_degrees_t hysteresis = 0.0f;

void setup() {
  Serial.begin(9600);
  Serial.println();
  Serial.println();

  Serial.print("Night start [hh UTC]: ");
  Serial.println(night_start);

  Serial.print("Night end [hh UTC]: ");
  Serial.println(night_end);

  if (!connect_wifi()) {
    Serial.println("Failed to connect to WiFi!");
  }
  
  if (!set_parameters()) {
    Serial.println("Failed to set thermostat parameters!");
  }

  sensors.begin();
  pinMode(heater_pin, OUTPUT);
  pinMode(led_pin, OUTPUT);

  set_power_led();
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

bool set_parameters() {
  bool success = true;
  
  requested_day_temperature = get_parameter(fields.requested_day_temperature, 15.0f);
  Serial.print("Requested day temperature [C]: ");
  Serial.println(requested_day_temperature);

  requested_night_temperature = get_parameter(fields.requested_night_temperature, 25.0f);
  Serial.print("Requested night temperature [C]: ");
  Serial.println(requested_night_temperature);
  
  hysteresis = get_parameter(fields.hysteresis, 4.0f);
  Serial.print("Hysteresis [C]: ");
  Serial.println(hysteresis);

  return success;
}

float get_parameter(const unsigned int field, const float default_value) {
  float data = 0.0f;
  data = read_field(field);
  if (data == 0) {
    Serial.print("Failed to read field ");
    Serial.print(field);
    Serial.println("! Leaving default value.");
    data = default_value;
  }
  return data;
}

float read_field(const unsigned int field) {
  return ThingSpeak.readFloatField(channel_id, field, read_api_key);
}

void set_power_led() {
  digitalWrite(led_pin, LOW);
}

void loop() {
  if (!should_post_update()) return;
  last_update_time = millis();

  if (!set_current_time()) {
    Serial.println("Failed to set current time!");
  }
  Serial.print("Current time [hh:mm:ss UTC]: ");
  Serial.println(time_client.getFormattedTime());

  if (!set_current_temperature()) {
    Serial.println("Failed to set current temperature!");
    return;
  }
  Serial.print("Current temperature [C]: ");
  Serial.println(current_temperature);

  if (!set_requested_temperature()) {
    Serial.println("Failed to set requested temperature!");
    return;
  }
  Serial.print("Requested temperature [C]: ");
  Serial.println(requested_temperature);

  if (!set_heater_state()) {
    Serial.println("Failed to set heater state!");
    return;
  }
  Serial.print("Current heater state: ");
  Serial.println(heater_state ? "enabled" : "disabled");

  if (!connect_wifi()) {
    Serial.println("Failed to connect to WiFi!");
    return;
  }

  if (!write_fields()) {
    Serial.println("Failed to write fields to ThingSpeak!");
    return;
  }
}

bool should_post_update() {
  return millis() - last_update_time >= posting_interval;
}

bool set_current_time() {
  bool success = false;
  Serial.println("Updating time...");
  for (unsigned int i = 1; i <= max_retries; ++i) {
    Serial.print("Attempt [");
    Serial.print(i);
    Serial.print("/");
    Serial.print(max_retries);
    Serial.println("]");
    if (time_client.update()) {
      success = true;
      Serial.println("OK");
      break;
    }
    delay(5000);
  }
  return success;
}

bool set_current_temperature() {
  bool success = true;
  current_temperature = get_temperature();
  if (current_temperature == DEVICE_DISCONNECTED_C) {
    Serial.println("Thermometer disconnected!");
    success = false;
  }
  return success;
}

celsius_degrees_t get_temperature() {
  sensors.requestTemperatures();
  const byte first_device = 0;
  celsius_degrees_t temperature = sensors.getTempCByIndex(first_device);
  return temperature;
}

bool set_requested_temperature() {
  bool success = true;
  requested_temperature = is_night() ? requested_night_temperature : requested_day_temperature;
  return success;
}

bool is_night() {
  hours_t hours = time_client.getHours();
  return hours >= night_start || hours < night_end;
}

bool set_heater_state() {
  bool success = true;
  if (current_temperature < requested_temperature) {
    heater_state = HIGH;
  } else if (current_temperature > requested_temperature + hysteresis) {
    heater_state = LOW;
  }
  digitalWrite(heater_pin, heater_state);
  return success;
}

bool write_fields() {
  ThingSpeak.setField(fields.current_temperature, current_temperature);
  ThingSpeak.setField(fields.heater_state, heater_state);
  ThingSpeak.setField(fields.requested_temperature, requested_temperature);
  return ThingSpeak.writeFields(channel_id, write_api_key);
}

