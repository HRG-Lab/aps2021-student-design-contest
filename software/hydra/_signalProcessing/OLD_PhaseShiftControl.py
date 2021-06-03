# Phase Shifter Module Control Software
#
# PSU BEAM Team 2021 - Rebecca DeSipio, Mike Shero, Ethan Tabler
#
# PROGRAM NOT IN USE - NOT SUPPORTED BY ADAFRUIT LIBRARIES
#
# This program requires a board with Raspberry Pi-compatible GPIO;
# for example, we are using the Odyssey SBC. (Dev on UDOO Bolt)
# It also requires the Adafruit MCP4725 Library:
#   > sudo pip3 install adafruit-circuitpython-mcp4725
#
# sudo apt-get install libgpiod2 python3-libgpiod gpiod

#import board
#import busio
import adafruit_mcp4725

# Initialize I2C bus.
#i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725.
dac = adafruit_mcp4725.MCP4725(address=0x62, busnum=1)
# Optionally you can specify a different address if you override the A0 pin.
# amp = adafruit_max9744.MAX9744(i2c, address=0x63)

# set 12-bit value for DAC output
dac.value = 65535
# range is 0 (minimum/ground) to 65535 (maximum/Vout).

# other output methods:
#     dac.normalized_value = 0.5  # ~1.65V output
#     dac.raw_output = 2047 # Also ~1.65V output
#
