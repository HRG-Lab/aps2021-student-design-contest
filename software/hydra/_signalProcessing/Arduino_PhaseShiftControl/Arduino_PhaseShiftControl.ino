/*
  Phase Shifter Module Control Software

  PSU BEAM Team 2021 - Rebecca DeSipio, Mike Shero, Ethan Tabler

  This program requires the Adafruit MCP4725 library to function.
*/

#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac;

void setup() {
  // init digital pins
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  
  // close existing connections before
  Serial.end();

  // initialize serial communication
  Serial.begin(9600);
  Serial.println("Serial connection initialized.");
  
  // This application uses the MCP4725(A2), not the Adafruit breakout board.
  // For the PSM's MCP4725A2 the address is 0x64 (default) or 0x65 (ADDR pin tied to VCC)
  // For MCP4725A0 the address is 0x60 or 0x61
  // For MCP4725A1 the address is 0x62 or 0x63 (Adafruit Breakout Board)
  dac.begin(0x65);

  // initialize A0 control pins and set all LOW
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  for (int i = 0, i <= 3, i++) {
        digitalWrite(i, LOW);
  }
}

void loop() {
  // see if there's incoming serial data
  if (Serial.available() > 0) {
    // look for the next valid integer in the incoming serial stream
    int dacVal = Serial.parseInt();

    // look for the newline --> end of sent value
    if (Serial.read() == '\n') {
     
      //dac.setVoltage((dacVal), false);

      // because there are 4 phase shifters (1 per channel), we must apply
      // the appropriate delta values to each module
      for (int i = 0, i <= 3, i++) {
        // apply delta value --> 0, 1*d, 2*d, 3*d
        digitalWrite(i, HIGH);
        delay(10);
        dac.setVoltage((i*dacVal), false);
        //Serial.println(dacVal);
        delay(10);
        digitalWrite(i, LOW);
      }
      
      dac.setVoltage(dacVal, false);
      Serial.println(dacVal);
     
    }

  }

}