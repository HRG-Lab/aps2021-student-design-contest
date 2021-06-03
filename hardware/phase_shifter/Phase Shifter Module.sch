EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Phase Shifter Module"
Date "2021-05-10"
Rev "1.0.0"
Comp "Penn State - Huff Research Group"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L SamacSys_Parts:JSPHS-661+ U1
U 1 1 5FC9612E
P 3200 4800
F 0 "U1" H 3850 5065 50  0000 C CNN
F 1 "JSPHS-661+" H 3850 4974 50  0000 C CNN
F 2 "SamacSys_Parts:JSPHS661" H 4350 4900 50  0001 L CNN
F 3 "https://www.minicircuits.com/pdfs/JSPHS-661+.pdf" H 4350 4800 50  0001 L CNN
F 4 "Narrow Band Phase Shifter, 50Ohm, 400 - 660 MHz" H 4350 4700 50  0001 L CNN "Description"
F 5 "6" H 4350 4600 50  0001 L CNN "Height"
F 6 "" H 4350 4500 50  0001 L CNN "Mouser Part Number"
F 7 "" H 4350 4400 50  0001 L CNN "Mouser Price/Stock"
F 8 "Mini-Circuits" H 4350 4300 50  0001 L CNN "Manufacturer_Name"
F 9 "JSPHS-661+" H 4350 4200 50  0001 L CNN "Manufacturer_Part_Number"
	1    3200 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 4800 4900 4800
Wire Wire Line
	4900 4800 4900 4900
Wire Wire Line
	4500 4900 4900 4900
Connection ~ 4900 4900
Wire Wire Line
	4900 4900 4900 5000
Wire Wire Line
	4500 5000 4900 5000
Connection ~ 4900 5000
Wire Wire Line
	4900 5000 4900 5100
Wire Wire Line
	4500 5100 4900 5100
Connection ~ 4900 5100
Wire Wire Line
	4900 5100 4900 5200
Wire Wire Line
	4500 5200 4900 5200
Connection ~ 4900 5200
Wire Wire Line
	4900 5200 4900 5300
Wire Wire Line
	4500 5300 4900 5300
Connection ~ 4900 5300
Wire Wire Line
	4900 5300 4900 5400
Wire Wire Line
	4500 5400 4900 5400
Text GLabel 2750 5100 0    50   Input ~ 0
V_Bias
Text GLabel 3050 4800 0    50   Input ~ 0
Signal_In
Wire Wire Line
	3050 4800 3200 4800
Text GLabel 6700 4800 2    50   Input ~ 0
Signal_Out
Text Notes 3400 5600 0    50   ~ 0
Tie bias lines together
$Comp
L power:GND #PWR0104
U 1 1 6011F112
P 4900 5450
F 0 "#PWR0104" H 4900 5200 50  0001 C CNN
F 1 "GND" H 4905 5277 50  0000 C CNN
F 2 "" H 4900 5450 50  0001 C CNN
F 3 "" H 4900 5450 50  0001 C CNN
	1    4900 5450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 5450 4900 5400
Connection ~ 4900 5400
$Comp
L NCP1117ST50T3G:NCP1117ST50T3G IC2
U 1 1 601543AA
P 8300 2500
F 0 "IC2" H 9200 2765 50  0000 C CNN
F 1 "NCP1117ST50T3G" H 9200 2674 50  0000 C CNN
F 2 "NCP1117ST50T3G:SOT230P700X180-4N" H 9950 2600 50  0001 L CNN
F 3 "http://www.onsemi.com/pub/Collateral/NCP1117-D.PDF" H 9950 2500 50  0001 L CNN
F 4 "ON SEMICONDUCTOR - NCP1117ST50T3G - LDO, REG, 20VIN, 1A, 5V, 1%, SOT223-3" H 9950 2400 50  0001 L CNN "Description"
F 5 "1.8" H 9950 2300 50  0001 L CNN "Height"
F 6 "ON Semiconductor" H 9950 2200 50  0001 L CNN "Manufacturer_Name"
F 7 "NCP1117ST50T3G" H 9950 2100 50  0001 L CNN "Manufacturer_Part_Number"
F 8 "863-NCP1117ST50T3G" H 9950 2000 50  0001 L CNN "Mouser Part Number"
F 9 "https://www.mouser.co.uk/ProductDetail/ON-Semiconductor/NCP1117ST50T3G?qs=Gev%252BmEvV0ib6dijy6U0dhQ%3D%3D" H 9950 1900 50  0001 L CNN "Mouser Price/Stock"
F 10 "NCP1117ST50T3G" H 9950 1800 50  0001 L CNN "Arrow Part Number"
F 11 "https://www.arrow.com/en/products/ncp1117st50t3g/on-semiconductor" H 9950 1700 50  0001 L CNN "Arrow Price/Stock"
	1    8300 2500
	1    0    0    -1  
$EndComp
Text GLabel 8250 2050 0    50   Input ~ 0
GND
Text GLabel 7450 1850 0    50   Input ~ 0
SDA
Text GLabel 7450 1950 0    50   Input ~ 0
SCL
$Comp
L power:GND #PWR0108
U 1 1 601649AD
P 7650 3200
F 0 "#PWR0108" H 7650 2950 50  0001 C CNN
F 1 "GND" H 7655 3027 50  0000 C CNN
F 2 "" H 7650 3200 50  0001 C CNN
F 3 "" H 7650 3200 50  0001 C CNN
	1    7650 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	7650 2500 7650 2600
Text GLabel 8200 2150 0    50   Input ~ 0
5V
Wire Notes Line
	7000 1000 7000 3650
Wire Notes Line
	7000 3650 10500 3650
Wire Notes Line
	10500 3650 10500 1000
Wire Notes Line
	10500 1000 7000 1000
Wire Notes Line
	6650 3650 6650 1000
Wire Notes Line
	6650 1000 1200 1000
Wire Notes Line
	1200 1000 1200 3650
Text Notes 5050 1250 2    138  ~ 0
DAC and V_bias Control
Text Notes 10450 1250 2    138  ~ 0
I2C Connector & 5V Regulation
Wire Notes Line
	1200 4000 1200 6000
Wire Notes Line
	1200 6000 8700 6000
Wire Notes Line
	8700 6000 8700 4000
Wire Notes Line
	8700 4000 1200 4000
Text Notes 5600 4250 2    138  ~ 0
Phase Shifter
$Comp
L Phase-Shifter-Module-rescue:CP1_Small-Device C1
U 1 1 60159CC7
P 7950 2600
F 0 "C1" V 7900 2500 50  0000 C CNN
F 1 "10uF" V 7900 2750 50  0000 C CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 7950 2600 50  0001 C CNN
F 3 "~" H 7950 2600 50  0001 C CNN
	1    7950 2600
	0    1    1    0   
$EndComp
$Comp
L Phase-Shifter-Module-rescue:CP1_Small-Device C2
U 1 1 6015B907
P 7950 2800
F 0 "C2" V 7900 2700 50  0000 C CNN
F 1 "10uF" V 7900 2950 50  0000 C CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 7950 2800 50  0001 C CNN
F 3 "~" H 7950 2800 50  0001 C CNN
	1    7950 2800
	0    1    1    0   
$EndComp
Wire Wire Line
	8300 2700 8300 2800
Wire Wire Line
	8300 2800 8050 2800
Wire Wire Line
	7650 2500 8300 2500
Wire Wire Line
	7850 2600 7650 2600
Connection ~ 7650 2600
Wire Wire Line
	7650 2600 7650 2800
Wire Wire Line
	7850 2800 7650 2800
Connection ~ 7650 2800
$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 6016A195
P 1650 4800
F 0 "J2" H 1850 4850 50  0000 C CNN
F 1 "Amphenol Edge Connector" H 1400 4950 50  0000 C CNN
F 2 "Amphenol Edge:Amphenol_132255_Edge" H 1650 4800 50  0001 C CNN
F 3 "~" H 1650 4800 50  0001 C CNN
	1    1650 4800
	-1   0    0    -1  
$EndComp
Text GLabel 2000 4800 2    50   Input ~ 0
Signal_In
Wire Wire Line
	1850 4800 2000 4800
$Comp
L power:+12V #PWR0109
U 1 1 6017B1E7
P 8400 2950
F 0 "#PWR0109" H 8400 2800 50  0001 C CNN
F 1 "+12V" H 8400 3100 50  0000 C CNN
F 2 "" H 8400 2950 50  0001 C CNN
F 3 "" H 8400 2950 50  0001 C CNN
	1    8400 2950
	1    0    0    -1  
$EndComp
$Comp
L Connector:Barrel_Jack J4
U 1 1 6017C5C3
P 9100 3200
F 0 "J4" H 8870 3158 50  0000 R CNN
F 1 "Barrel_Jack" H 8870 3249 50  0000 R CNN
F 2 "Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal" H 9150 3160 50  0001 C CNN
F 3 "~" H 9150 3160 50  0001 C CNN
	1    9100 3200
	-1   0    0    1   
$EndComp
Wire Wire Line
	8800 3300 8400 3300
Wire Wire Line
	7650 2800 7650 3100
Wire Wire Line
	7650 3100 8800 3100
Connection ~ 7650 3100
Wire Wire Line
	7650 3100 7650 3200
Text GLabel 7900 4800 0    50   Input ~ 0
Signal_Out
$Comp
L power:GND #PWR0102
U 1 1 601B8A6D
P 7950 5000
F 0 "#PWR0102" H 7950 4750 50  0001 C CNN
F 1 "GND" H 7955 4827 50  0000 C CNN
F 2 "" H 7950 5000 50  0001 C CNN
F 3 "" H 7950 5000 50  0001 C CNN
	1    7950 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 4900 1950 4900
Wire Wire Line
	1950 4900 1950 5000
$Comp
L power:GND #PWR0110
U 1 1 601F96CD
P 1950 5000
F 0 "#PWR0110" H 1950 4750 50  0001 C CNN
F 1 "GND" H 1955 4827 50  0000 C CNN
F 2 "" H 1950 5000 50  0001 C CNN
F 3 "" H 1950 5000 50  0001 C CNN
	1    1950 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	8400 3300 8400 3000
Wire Wire Line
	8300 2800 8300 3000
Wire Wire Line
	8300 3000 8400 3000
Connection ~ 8300 2800
Connection ~ 8400 3000
Wire Wire Line
	8400 3000 8400 2950
$Comp
L Device:R R3
U 1 1 601802C2
P 7600 2150
F 0 "R3" H 7670 2196 50  0000 L CNN
F 1 "10k" H 7670 2105 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 7530 2150 50  0001 C CNN
F 3 "~" H 7600 2150 50  0001 C CNN
	1    7600 2150
	1    0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 60181058
P 7850 2150
F 0 "R4" H 7920 2196 50  0000 L CNN
F 1 "10k" H 7920 2105 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 7780 2150 50  0001 C CNN
F 3 "~" H 7850 2150 50  0001 C CNN
	1    7850 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 1950 7850 1950
Wire Wire Line
	7450 1850 7600 1850
Wire Wire Line
	7600 2350 7850 2350
Wire Wire Line
	7600 2300 7600 2350
Wire Wire Line
	7850 2300 7850 2350
Connection ~ 7850 2350
Wire Wire Line
	7850 2350 8250 2350
Wire Wire Line
	7850 2000 7850 1950
Connection ~ 7850 1950
Wire Wire Line
	7850 1950 8500 1950
Wire Wire Line
	7600 2000 7600 1850
Connection ~ 7600 1850
Wire Wire Line
	7600 1850 8500 1850
$Comp
L SamacSys_Parts:JSPHS-661+ U2
U 1 1 601B4F51
P 6550 5400
F 0 "U2" H 7200 4550 50  0000 C CNN
F 1 "JSPHS-661+" H 7200 4650 50  0000 C CNN
F 2 "SamacSys_Parts:JSPHS661" H 7700 5500 50  0001 L CNN
F 3 "https://www.minicircuits.com/pdfs/JSPHS-661+.pdf" H 7700 5400 50  0001 L CNN
F 4 "Narrow Band Phase Shifter, 50Ohm, 400 - 660 MHz" H 7700 5300 50  0001 L CNN "Description"
F 5 "6" H 7700 5200 50  0001 L CNN "Height"
F 6 "" H 7700 5100 50  0001 L CNN "Mouser Part Number"
F 7 "" H 7700 5000 50  0001 L CNN "Mouser Price/Stock"
F 8 "Mini-Circuits" H 7700 4900 50  0001 L CNN "Manufacturer_Name"
F 9 "JSPHS-661+" H 7700 4800 50  0001 L CNN "Manufacturer_Part_Number"
	1    6550 5400
	-1   0    0    1   
$EndComp
Wire Wire Line
	5250 4800 4900 4800
Connection ~ 4900 4800
Wire Wire Line
	5250 4900 4900 4900
Wire Wire Line
	5250 5000 4900 5000
Wire Wire Line
	5250 5100 4900 5100
Wire Wire Line
	5250 5200 4900 5200
Wire Wire Line
	5250 5300 4900 5300
Wire Wire Line
	5250 5400 4900 5400
$Comp
L Connector_Generic:Conn_01x02 J3
U 1 1 601AC82E
P 8250 4800
F 0 "J3" H 8450 4850 50  0000 C CNN
F 1 "Amphenol Edge Connector" H 8000 4950 50  0000 C CNN
F 2 "Amphenol Edge:Amphenol_132255_Edge" H 8250 4800 50  0001 C CNN
F 3 "~" H 8250 4800 50  0001 C CNN
	1    8250 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	8050 4900 7950 4900
Wire Wire Line
	7950 4900 7950 5000
Wire Wire Line
	8050 4800 7900 4800
Wire Wire Line
	6700 4800 6550 4800
Text GLabel 7100 5100 2    50   Input ~ 0
V_Bias
Wire Wire Line
	6550 5100 6650 5100
Wire Wire Line
	6550 4900 6650 4900
Wire Wire Line
	6650 4900 6650 5100
Connection ~ 6650 5100
Wire Wire Line
	6650 5100 7100 5100
Wire Wire Line
	3200 5400 3100 5400
Wire Wire Line
	3100 5400 3100 5700
Wire Wire Line
	3100 5700 6650 5700
Wire Wire Line
	6650 5700 6650 5400
Wire Wire Line
	6650 5400 6550 5400
Text Notes 5450 5600 0    50   ~ 0
Tie bias lines together
Text Notes 3900 5800 0    50   ~ 0
'OUT' of U1 goes to 'IN' of U2, both share bias lines
Wire Wire Line
	6550 5000 6900 5000
Wire Wire Line
	6900 5000 6900 5200
Wire Wire Line
	6900 5300 6550 5300
Wire Wire Line
	6550 5200 6900 5200
Connection ~ 6900 5200
Wire Wire Line
	6900 5200 6900 5300
$Comp
L power:GND #PWR0107
U 1 1 60239150
P 6900 5400
F 0 "#PWR0107" H 6900 5150 50  0001 C CNN
F 1 "GND" H 6905 5227 50  0000 C CNN
F 2 "" H 6900 5400 50  0001 C CNN
F 3 "" H 6900 5400 50  0001 C CNN
	1    6900 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 5300 6900 5400
Connection ~ 6900 5300
Wire Wire Line
	3200 5100 3100 5100
Wire Wire Line
	3200 5300 3100 5300
Wire Wire Line
	3100 5300 3100 5100
Connection ~ 3100 5100
Wire Wire Line
	3100 5100 2750 5100
Wire Wire Line
	3200 4900 2850 4900
Wire Wire Line
	2850 4900 2850 5000
Wire Wire Line
	3200 5200 2850 5200
Connection ~ 2850 5200
Wire Wire Line
	2850 5200 2850 5400
Wire Wire Line
	3200 5000 2850 5000
Connection ~ 2850 5000
Wire Wire Line
	2850 5000 2850 5200
$Comp
L power:GND #PWR0111
U 1 1 602629C9
P 2850 5400
F 0 "#PWR0111" H 2850 5150 50  0001 C CNN
F 1 "GND" H 2855 5227 50  0000 C CNN
F 2 "" H 2850 5400 50  0001 C CNN
F 3 "" H 2850 5400 50  0001 C CNN
	1    2850 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	10100 2500 10150 2500
Text GLabel 8250 1750 0    50   Input ~ 0
A0
Wire Wire Line
	8250 2050 8500 2050
Wire Wire Line
	8200 2150 8250 2150
Wire Wire Line
	8050 2600 8250 2600
Wire Wire Line
	8250 2600 8250 2350
Connection ~ 8250 2600
Wire Wire Line
	8250 2600 8300 2600
Connection ~ 8250 2150
Wire Wire Line
	8250 2150 8500 2150
Connection ~ 8250 2350
Wire Wire Line
	8250 2350 8250 2150
Wire Wire Line
	8250 1750 8350 1750
$Comp
L Device:R R5
U 1 1 606CD92C
P 8350 1600
F 0 "R5" H 8420 1646 50  0000 L CNN
F 1 "10k" H 8420 1555 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 8280 1600 50  0001 C CNN
F 3 "~" H 8350 1600 50  0001 C CNN
	1    8350 1600
	1    0    0    -1  
$EndComp
Text GLabel 8250 1450 0    50   Input ~ 0
GND
Connection ~ 8350 1750
Wire Wire Line
	8350 1750 8500 1750
Wire Wire Line
	8250 1450 8350 1450
Text GLabel 10150 2500 2    50   Input ~ 0
5V
Wire Notes Line
	10500 4000 10500 6000
Wire Notes Line
	10500 6000 9000 6000
Wire Notes Line
	9000 6000 9000 4000
Wire Notes Line
	9000 4000 10500 4000
Text Notes 9200 4200 0    79   ~ 0
Surface Test Pads
Text GLabel 9400 4550 0    50   Input ~ 0
GND
Text GLabel 9400 5150 0    50   Input ~ 0
V_DAC
Text GLabel 9400 5450 0    50   Input ~ 0
V_Bias
Text GLabel 9400 4700 0    50   Input ~ 0
5V
Text GLabel 8300 3000 0    50   Input ~ 0
12V
Text GLabel 9400 4850 0    50   Input ~ 0
12V
$Comp
L Connector_Generic:Conn_01x01 V_DAC1
U 1 1 60970B5C
P 9800 5100
F 0 "V_DAC1" H 9880 5142 50  0000 L CNN
F 1 "Conn_01x01" H 9880 5051 50  0000 L CNN
F 2 "Phase Shifter Module:TestPad_Medium" H 9800 5100 50  0001 C CNN
F 3 "~" H 9800 5100 50  0001 C CNN
	1    9800 5100
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 V_Bias1
U 1 1 6097272E
P 9800 5500
F 0 "V_Bias1" H 9880 5542 50  0000 L CNN
F 1 "Conn_01x01" H 9880 5451 50  0000 L CNN
F 2 "Phase Shifter Module:TestPad_Medium" H 9800 5500 50  0001 C CNN
F 3 "~" H 9800 5500 50  0001 C CNN
	1    9800 5500
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 GND1
U 1 1 60976621
P 9800 4500
F 0 "GND1" H 9880 4542 50  0000 L CNN
F 1 "Conn_01x01" H 9880 4451 50  0000 L CNN
F 2 "Phase Shifter Module:TestPad_Medium" H 9800 4500 50  0001 C CNN
F 3 "~" H 9800 4500 50  0001 C CNN
	1    9800 4500
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 5V1
U 1 1 60976627
P 9800 4700
F 0 "5V1" H 9880 4742 50  0000 L CNN
F 1 "Conn_01x01" H 9880 4651 50  0000 L CNN
F 2 "Phase Shifter Module:TestPad_Medium" H 9800 4700 50  0001 C CNN
F 3 "~" H 9800 4700 50  0001 C CNN
	1    9800 4700
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 12V1
U 1 1 6097662D
P 9800 4900
F 0 "12V1" H 9880 4942 50  0000 L CNN
F 1 "Conn_01x01" H 9880 4851 50  0000 L CNN
F 2 "Phase Shifter Module:TestPad_Medium" H 9800 4900 50  0001 C CNN
F 3 "~" H 9800 4900 50  0001 C CNN
	1    9800 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	9400 4550 9500 4550
Wire Wire Line
	9500 4550 9500 4500
Wire Wire Line
	9500 4500 9600 4500
Wire Wire Line
	9400 4700 9600 4700
Wire Wire Line
	9400 4850 9500 4850
Wire Wire Line
	9500 4850 9500 4900
Wire Wire Line
	9500 4900 9600 4900
Wire Wire Line
	9400 5150 9500 5150
Wire Wire Line
	9500 5150 9500 5100
Wire Wire Line
	9500 5100 9600 5100
Wire Wire Line
	9400 5450 9500 5450
Wire Wire Line
	9500 5450 9500 5500
Wire Wire Line
	9500 5500 9600 5500
$Comp
L Device:LED D1
U 1 1 6089E3C9
P 9900 1900
F 0 "D1" V 9939 1782 50  0000 R CNN
F 1 "PWR_LED" V 9848 1782 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 9900 1900 50  0001 C CNN
F 3 "~" H 9900 1900 50  0001 C CNN
	1    9900 1900
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R6
U 1 1 608A133D
P 9700 1700
F 0 "R6" V 9493 1700 50  0000 C CNN
F 1 "620" V 9584 1700 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 9630 1700 50  0001 C CNN
F 3 "~" H 9700 1700 50  0001 C CNN
	1    9700 1700
	0    1    1    0   
$EndComp
Text GLabel 9500 1700 0    50   Input ~ 0
5V
Text GLabel 9850 2150 0    50   Input ~ 0
GND
Wire Wire Line
	9500 1700 9550 1700
Wire Wire Line
	9850 1700 9900 1700
Wire Wire Line
	9900 1700 9900 1750
Wire Wire Line
	9900 2050 9900 2150
Wire Wire Line
	9900 2150 9850 2150
$Comp
L SamacSys_Parts:LMC6081IMX_NOPB IC3
U 1 1 608AEA7A
P 3900 2300
F 0 "IC3" H 5050 2565 50  0000 C CNN
F 1 "LM741CN_NOPB" H 5050 2474 50  0000 C CNN
F 2 "Package_SO:SOP-8_3.9x4.9mm_P1.27mm" H 6050 2400 50  0001 L CNN
F 3 "" H 6050 2300 50  0001 L CNN
F 4 "LM741 Operational Amplifier 1MHz DIP8 Texas Instruments LM741CN/NOPB Op Amp, 1MHz, 8-Pin MDIP" H 6050 2200 50  0001 L CNN "Description"
F 5 "5.08" H 6050 2100 50  0001 L CNN "Height"
F 6 "926-LM741CN/NOPB" H 6050 2000 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/Texas-Instruments/LM741CN-NOPB?qs=QbsRYf82W3Gt6%252BDX6%252BuAjw%3D%3D" H 6050 1900 50  0001 L CNN "Mouser Price/Stock"
F 8 "Texas Instruments" H 6050 1800 50  0001 L CNN "Manufacturer_Name"
F 9 "LM741CN/NOPB" H 6050 1700 50  0001 L CNN "Manufacturer_Part_Number"
	1    3900 2300
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR0101
U 1 1 608EEC2D
P 6000 2300
F 0 "#PWR0101" H 6000 2150 50  0001 C CNN
F 1 "+12V" H 6015 2473 50  0000 C CNN
F 2 "" H 6000 2300 50  0001 C CNN
F 3 "" H 6000 2300 50  0001 C CNN
	1    6000 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	6000 2300 6000 2400
Wire Wire Line
	6000 2400 5900 2400
Wire Wire Line
	5900 2500 6150 2500
Wire Wire Line
	6150 2500 6150 1950
$Comp
L SamacSys_Parts:ERA-6AED1402V R2
U 1 1 609169EB
P 4700 1950
F 0 "R2" H 5150 1850 50  0000 C CNN
F 1 "10k" H 4950 1850 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 4630 1950 50  0001 C CNN
F 3 "~" H 4700 1950 50  0001 C CNN
	1    4700 1950
	-1   0    0    1   
$EndComp
Wire Wire Line
	4000 1950 3750 1950
Wire Wire Line
	3750 1950 3750 2400
Wire Wire Line
	3750 2400 3900 2400
Wire Wire Line
	3900 2500 3650 2500
$Comp
L power:GND #PWR0103
U 1 1 60935F6A
P 3900 3000
F 0 "#PWR0103" H 3900 2750 50  0001 C CNN
F 1 "GND" H 3905 2827 50  0000 C CNN
F 2 "" H 3900 3000 50  0001 C CNN
F 3 "" H 3900 3000 50  0001 C CNN
	1    3900 3000
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 60938805
P 3750 2750
F 0 "R1" H 3550 2800 50  0000 L CNN
F 1 "10k" H 3550 2700 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 3680 2750 50  0001 C CNN
F 3 "~" H 3750 2750 50  0001 C CNN
	1    3750 2750
	1    0    0    -1  
$EndComp
Text GLabel 1550 2450 0    50   Input ~ 0
GND
$Comp
L power:GND #PWR0106
U 1 1 601423DC
P 1600 2500
F 0 "#PWR0106" H 1600 2250 50  0001 C CNN
F 1 "GND" H 1605 2327 50  0000 C CNN
F 2 "" H 1600 2500 50  0001 C CNN
F 3 "" H 1600 2500 50  0001 C CNN
	1    1600 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	1550 2450 1600 2450
Connection ~ 1600 2450
Wire Wire Line
	1600 2450 1900 2450
Wire Wire Line
	1600 2500 1600 2450
Wire Wire Line
	1850 2350 1900 2350
$Comp
L SamacSys_Parts:MCP4725A2T-E_CH IC1
U 1 1 6064401B
P 1900 2350
F 0 "IC1" H 2450 2615 50  0000 C CNN
F 1 "MCP4725A2T-E_CH" H 2450 2524 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6_Handsoldering" H 2850 2450 50  0001 L CNN
F 3 "http://ww1.microchip.com/downloads/en/devicedoc/22039d.pdf" H 2850 2350 50  0001 L CNN
F 4 "Microchip MCP4725A2T-E/CH, 12 bit Serial DAC, 3.4Msps, 6-Pin SOT-23" H 2850 2250 50  0001 L CNN "Description"
F 5 "1.45" H 2850 2150 50  0001 L CNN "Height"
F 6 "579-MCP4725A2T-E/CH" H 2850 2050 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/Microchip-Technology/MCP4725A2T-E-CH?qs=hH%252BOa0VZEiABOw9BMlFjfA%3D%3D" H 2850 1950 50  0001 L CNN "Mouser Price/Stock"
F 8 "Microchip" H 2850 1850 50  0001 L CNN "Manufacturer_Name"
F 9 "MCP4725A2T-E/CH" H 2850 1750 50  0001 L CNN "Manufacturer_Part_Number"
	1    1900 2350
	1    0    0    -1  
$EndComp
Text GLabel 3050 2350 2    50   Input ~ 0
A0
Wire Wire Line
	3000 2350 3050 2350
Text GLabel 1850 2350 0    50   Input ~ 0
V_DAC
Wire Notes Line
	1200 3650 6650 3650
Wire Wire Line
	3000 2450 3050 2450
Wire Wire Line
	3050 2550 3000 2550
Text GLabel 3050 2450 2    50   Input ~ 0
SCL
Text GLabel 3050 2550 2    50   Input ~ 0
SDA
Text GLabel 1850 2550 0    50   Input ~ 0
5V
Wire Wire Line
	1850 2550 1900 2550
Wire Wire Line
	3750 2600 3750 2400
Connection ~ 3750 2400
Wire Wire Line
	3750 2900 3900 2900
Wire Wire Line
	3900 2900 3900 2600
Wire Wire Line
	3900 3000 3900 2900
Connection ~ 3900 2900
Text Notes 2300 2750 0    50   ~ 0
I2C DAC
Text Notes 4500 2800 0    50   ~ 0
Configured for Gain = 2
Text GLabel 3650 2500 0    50   Input ~ 0
V_DAC
Text GLabel 6250 2500 2    50   Input ~ 0
V_Bias
Wire Wire Line
	6150 2500 6250 2500
Connection ~ 6150 2500
Wire Wire Line
	6150 1950 4700 1950
$Comp
L Connector:Screw_Terminal_01x05 J1
U 1 1 609D35EE
P 8700 1950
F 0 "J1" H 8780 1992 50  0000 L CNN
F 1 "Screw_Terminal_01x05" H 8780 1901 50  0000 L CNN
F 2 "TerminalBlock_TE-Connectivity:TerminalBlock_TE_282834-5_1x05_P2.54mm_Horizontal" H 8700 1950 50  0001 C CNN
F 3 "~" H 8700 1950 50  0001 C CNN
	1    8700 1950
	1    0    0    -1  
$EndComp
$EndSCHEMATC
