/**

   @todo
    - move strings to flash (less RAM consumption)
    - fix deprecated convertation form string to char* startAsTag
    - give example description
*/
#include <SPI.h>
//#include <Wire.h>
#include "DW1000Ranging.h"

// connection pins

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is 
const uint8_t PIN_RST = 9; // reset pin
const uint8_t PIN_IRQ = 2; // irq pin
const uint8_t PIN_SS = 10; // spi select pin
uint16_t count = 0;
float range = 0.1;
void setup() {
//  Wifi.begin();
//  Wifi.close();
  Serial.begin(9600);
  delay(1000);
  //init the configuration
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ); //Reset, CS, IRQ pin
//  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachNewDevice(newDevice);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
//  //Enable the filter to smooth the distance
  DW1000Ranging.useRangeFilter(true);
//
//  //we start the module as a tag
  DW1000Ranging.startAsTag("7A:FF:22:EA:82:60:3B:9A", DW1000.MODE_LONGDATA_RANGE_ACCURACY);
  Serial.print("\n");
  
//  Wifi.begin();
//  Wifi.println("REST - 18748"); 
//  delay(1000);
}

void loop() {
  DW1000Ranging.loop();
//  arr[count] = 0;
//  Serial.println(range);
//  range = range + 0.1;
//  Serial.println(count);
}


void newRange() {
//    range = DW1000Ranging.getDistantDevice()->getRange();
    Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
    Serial.print(" ");
    Serial.println(DW1000Ranging.getDistantDevice()->getRange());
}

void newDevice(DW1000Device* device) {
  //  Serial.print("ranging init; 1 device added ! ->");
  //  Serial.print(" short:");
  //  Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device* device) {
  //  Serial.print("delete inactive device:");
  //  Serial.println(device->getShortAddress(), HEX);
}

