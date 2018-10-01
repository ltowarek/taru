#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

ADC_MODE(ADC_VCC);

Adafruit_BMP280 bme;

const char *ssid = "";
const char *password = "";
const char *mqtt_server = "";
const char *mqtt_user = "";
const char *mqtt_password = "";
const char *mqtt_client = "sensor/balcony";
const char *mqtt_temperature_topic = "sensor/balcony/temperature";
const char *mqtt_pressure_topic = "sensor/balcony/pressure";
const char *mqtt_voltage_topic = "sensor/balcony/voltage";

const uint64_t sleep_duration = 60e6;

WiFiClient wifi;
PubSubClient mqtt(wifi);

void setup() {
  if (!bme.begin(0x77)) {
    ESP.deepSleep(sleep_duration);
    delay(500);
  }
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(10);
  }
  
  mqtt.setServer(mqtt_server, 1883);
  mqtt.connect(mqtt_client, mqtt_user, mqtt_password);
  while (!mqtt.connected()) {
    delay(10);
  }
  
  float temperature = bme.readTemperature();
  float pressure = bme.readPressure();
  float voltage = (float)(ESP.getVcc()) / 1024.0f;
  
  mqtt.publish(mqtt_temperature_topic, String(temperature).c_str());
  mqtt.publish(mqtt_pressure_topic, String(pressure).c_str());
  mqtt.publish(mqtt_voltage_topic, String(voltage).c_str());
  delay(500);

  mqtt.disconnect();
  while (mqtt.connected()) {
    delay(10);
  }
  
  wifi.stop();
  while (wifi.connected()) {
    delay(10);
  }
  
  ESP.deepSleep(sleep_duration);
  delay(500);
}

void loop() {
}
