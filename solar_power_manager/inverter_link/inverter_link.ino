const int trigger_pin = D8;

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

void setup() {
  Serial.begin(2400);
  pinMode(trigger_pin, INPUT);
}

void loop() {
  if (Serial.available()) {
    char in = (char)Serial.read();
    if (in == '(') {
      current_byte_id = 0;
      current_token_id = 0;
      Serial.println();
    } else {
      if (current_byte_id == tokens[current_token_id].end) {
        Serial.print(tokens[current_token_id].name);
        Serial.print(": ");
        Serial.println(current_token_value);
        current_token_id++;
      }
      if (current_byte_id == tokens[current_token_id].start) {
        current_token_value = "";
      }
      current_token_value += in;
    }
    current_byte_id++;
  }

  if (digitalRead(trigger_pin)) {
    Serial.write(0x51);
    Serial.write(0x50);
    Serial.write(0x49);
    Serial.write(0x47);
    Serial.write(0x53);
    Serial.write(0xb7);
    Serial.write(0xa9);
    Serial.write(0x0d);
    delay(1000);
  }
}

