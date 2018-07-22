#include <ESP8266WiFi.h>
#include <PubSubClient.h>

struct ResponseToken {
  const char name[100];
  const unsigned int start;  // inclusive
  const unsigned int end;  // exclusive
};

const ResponseToken tokens[] = {
  {"grid_voltage", 1, 6},
  {"grid_frequency", 7, 11},
  {"ac_output_voltage", 12, 17},
  {"ac_output_frequency", 18, 22},
  {"ac_output_apparent_power", 23, 27},
  {"ac_output_active_power", 28, 32},
  {"output_load_percent", 33, 36},
  {"bus_voltage", 37, 40},
  {"battery_voltage", 41, 46},
  {"battery_charging_current", 47, 50},
  {"battery_capacity", 51, 54},
  {"inverter_heat_sink_temperature", 55, 59},
  {"pv_input_current_for_battery", 60, 64},
  {"pv_input_voltage", 65, 70},
  {"battery_voltage_from_scc", 71, 76},
  {"battery_discharge_current", 77, 82},
  {"is_sbu_priority_version_added", 83, 84},
  {"is_configuration_changed", 84, 85},
  {"is_scc_firmware_updated", 85, 86},
  {"is_load_on", 86, 87},
  {"is_battery_voltage_to_steady_while_charging", 87, 88},
  {"is_charging_on", 88, 89},
  {"is_scc_charging_on", 89, 90},
  {"is_ac_charging_on", 90, 91},
  {"battery_voltage_offset_for_fans_on", 92, 94},
  {"eeprom_version", 95, 97},
  {"pv_charging_power", 98, 103},
  {"is_charging_to_floating_enabled", 104, 105},
  {"is_switch_on", 105, 106},
  {"is_dustproof_installed", 106, 107}
};

unsigned int current_byte_id = 0;
unsigned int current_token_id = 0;
String current_token_value = "";

const char *ssid = "";
const char *password = "";
const char *mqtt_server = "";
const char *mqtt_client = "inverter_link";
const char *mqtt_request_topic = "inverter/request";
const char *mqtt_response_topic = "inverter/response";
const char *mqtt_log_topic = "inverter/log";

WiFiClient wifi;
PubSubClient mqtt(wifi);

void callback(char *topic, byte *payload, unsigned int length) {
  String command = "";
  for (unsigned int i = 0; i < length; ++i) {
    command += (char)payload[i];
  }
  if (command == "QPIGS") {
    Serial.write(0x51);
    Serial.write(0x50);
    Serial.write(0x49);
    Serial.write(0x47);
    Serial.write(0x53);
    Serial.write(0xb7);
    Serial.write(0xa9);
    Serial.write(0x0d);
  }
}

void reconnect() {
  while (!mqtt.connected()) {
    if (mqtt.connect(mqtt_client)) {
      mqtt.publish(mqtt_log_topic, "Connected to MQTT server");
      mqtt.subscribe(mqtt_request_topic);
    } else {
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(2400);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  mqtt.setServer(mqtt_server, 1883);
  mqtt.setCallback(callback);
}

void loop() {
  if (!mqtt.connected()) {
    reconnect();
  }
  mqtt.loop();
  
  if (Serial.available()) {
    char in = (char)Serial.read();
    if (in == '(') {
      current_byte_id = 0;
      current_token_id = 0;
    } else {
      if (current_byte_id == tokens[current_token_id].end) {
        mqtt.publish(mqtt_log_topic, "Sending response");
        String topic = mqtt_response_topic + String('/') + String(tokens[current_token_id].name);
        mqtt.publish(topic.c_str(), current_token_value.c_str());
        current_token_id++;
      }
      if (current_byte_id == tokens[current_token_id].start) {
        current_token_value = "";
      }
      current_token_value += in;
    }
    current_byte_id++;
  }
}

