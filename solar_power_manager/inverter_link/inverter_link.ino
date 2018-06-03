String command_string = "";
bool command_read = false;

void setup() {
  Serial.begin(2400);
}

void loop() {
  if (Serial.available()) {
    char in = (char)Serial.read();
    if (in == '\r') {
      command_read = true;
      Serial.print("Command read: ");
      Serial.println(command_string);
    } else {
      command_string += in;
    }
  }

  if (command_read && command_string == "QPIGS") {
    Serial.write(0x51);
    Serial.write(0x50);
    Serial.write(0x49);
    Serial.write(0x47);
    Serial.write(0x53);
    Serial.write(0xb7);
    Serial.write(0xa9);
    Serial.write(0x0d);
  }

  if (command_read) {
    command_read = false;
    command_string = "";
  }
}

