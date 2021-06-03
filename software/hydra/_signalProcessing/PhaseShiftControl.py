# Phase Shifter Module Control Software
#
# PSU BEAM Team 2021 - Rebecca DeSipio, Mike Shero, Ethan Tabler
#
#
#

import serial

# Start a serial connection on port ACM0 with the built-in Arduino Leonardo (Bolt)
# ONLY FOR TESTING - This will be initialized in the hydra_signal_processor file
'''
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

while True:
    dacVal = int(input("Enter a value between 0 and 4095: "))
    if (dacVal >= 0) and (dacVal <= 4095):
        # Write value to serial port
        arduino.write((str(dacVal) + '\n').encode())

    else:
        print("Please enter a valid number.")
'''


def phaseShift(deltaVal, arduino, side):
    # TODO: Map deltaVal (degrees) to corresponding dacVal (0 to 4095)
    dacVal = 128 * deltaVal

    if side == "l":
        # Write value to serial port
        arduino.write((str(dacVal) + 'l' + '\n').encode())
        
    elif side == "r":
        # Write value to serial port
        arduino.write((str(dacVal) + 'r' + '\n').encode())

