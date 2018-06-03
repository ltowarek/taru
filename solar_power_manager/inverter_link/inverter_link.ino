String command_string = "";
bool command_read = false;
const int trigger_pin = D8;

void setup() {
  Serial.begin(2400);
  pinMode(trigger_pin, INPUT);
}

void loop() {
  if (Serial.available()) {
    char in = (char)Serial.read();
    if (in == '\r') {
      command_read = true;
    } else {
      command_string += in;
    }
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

  if (command_read) {
    Serial.println();
    Serial.print("Command: ");
    Serial.println(command_string);
    Serial.println();
    
    const String grid_voltage = command_string.substring(1, 6);
    Serial.print("grid_voltage: ");
    Serial.println(grid_voltage);
    
    const String grid_frequency = command_string.substring(7, 11);
    Serial.print("grid_frequency: ");
    Serial.println(grid_frequency);

    const String ac_output_voltage = command_string.substring(12, 17);
    Serial.print("ac_output_voltage: ");
    Serial.println(ac_output_voltage);
    
    const String ac_output_frequency = command_string.substring(18, 22);
    Serial.print("ac_output_frequency: ");
    Serial.println(ac_output_frequency);
    
    const String ac_output_apparent_power = command_string.substring(23, 27);
    Serial.print("ac_output_apparent_power: ");
    Serial.println(ac_output_apparent_power);

    const String ac_output_active_power = command_string.substring(28, 32);
    Serial.print("ac_output_active_power: ");
    Serial.println(ac_output_active_power);
    
    const String output_load_percent = command_string.substring(33, 36);
    Serial.print("output_load_percent: ");
    Serial.println(output_load_percent);
    
    const String bus_voltage = command_string.substring(37, 40);
    Serial.print("bus_voltage: ");
    Serial.println(bus_voltage);

    const String battery_voltage = command_string.substring(41, 46);
    Serial.print("battery_voltage: ");
    Serial.println(battery_voltage);

    const String battery_charging_current = command_string.substring(47, 50);
    Serial.print("battery_charging_current: ");
    Serial.println(battery_charging_current);

    const String battery_capacity = command_string.substring(51, 54);
    Serial.print("battery_capacity: ");
    Serial.println(battery_capacity);

    const String inverter_heat_sink_temperature = command_string.substring(55, 59);
    Serial.print("inverter_heat_sink_temperature: ");
    Serial.println(inverter_heat_sink_temperature);

    const String pv_input_current_for_battery = command_string.substring(60, 64);
    Serial.print("pv_input_current_for_battery: ");
    Serial.println(pv_input_current_for_battery);

    const String pv_input_voltage = command_string.substring(65, 70);
    Serial.print("pv_input_voltage: ");
    Serial.println(pv_input_voltage);

    const String battery_voltage_from_scc = command_string.substring(71, 76);
    Serial.print("battery_voltage_from_scc: ");
    Serial.println(battery_voltage_from_scc);

    const String battery_discharge_current = command_string.substring(77, 82);
    Serial.print("battery_discharge_current: ");
    Serial.println(battery_discharge_current);

    const String is_sbu_priority_version_added = command_string.substring(83, 84);
    Serial.print("is_sbu_priority_version_added: ");
    Serial.println(is_sbu_priority_version_added);

    const String is_configuration_changed = command_string.substring(84, 85);
    Serial.print("is_configuration_changed: ");
    Serial.println(is_configuration_changed);

    const String is_scc_firmware_updated = command_string.substring(85, 86);
    Serial.print("is_scc_firmware_updated: ");
    Serial.println(is_scc_firmware_updated);

    const String is_load_on = command_string.substring(86, 87);
    Serial.print("is_load_on: ");
    Serial.println(is_load_on);

    const String is_battery_voltage_to_steady_while_charging = command_string.substring(87, 88);
    Serial.print("is_battery_voltage_to_steady_while_charging: ");
    Serial.println(is_battery_voltage_to_steady_while_charging);

    const String is_charging_on = command_string.substring(88, 89);
    Serial.print("is_charging_on: ");
    Serial.println(is_charging_on);

    const String is_scc_charging_on = command_string.substring(89, 90);
    Serial.print("is_scc_charging_on: ");
    Serial.println(is_scc_charging_on);

    const String is_ac_charging_on = command_string.substring(90, 91);
    Serial.print("is_ac_charging_on: ");
    Serial.println(is_ac_charging_on);
    
    const String battery_voltage_offset_for_fans_on = command_string.substring(92, 94);
    Serial.print("battery_voltage_offset_for_fans_on: ");
    Serial.println(battery_voltage_offset_for_fans_on);

    const String eeprom_version = command_string.substring(95, 97);
    Serial.print("eeprom_version: ");
    Serial.println(eeprom_version);

    const String pv_charging_power = command_string.substring(98, 103);
    Serial.print("pv_charging_power: ");
    Serial.println(pv_charging_power);

    const String is_charging_to_floating_enabled = command_string.substring(104, 105);
    Serial.print("is_charging_to_floating_enabled: ");
    Serial.println(is_charging_to_floating_enabled);

    const String is_switch_on = command_string.substring(105, 106);
    Serial.print("is_switch_on: ");
    Serial.println(is_switch_on);

    const String is_dustproof_installed = command_string.substring(106, 107);
    Serial.print("is_dustproof_installed: ");
    Serial.println(is_dustproof_installed);
    
    command_read = false;
    command_string = "";
  }
}

