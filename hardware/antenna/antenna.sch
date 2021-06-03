EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector_Generic:Conn_01x01 J1
U 1 1 602D36F3
P 4500 3000
F 0 "J1" H 4418 2775 50  0000 C CNN
F 1 "Conn_01x01" H 4418 2866 50  0000 C CNN
F 2 "Antenna_Clamp_Adapter:Wire_Clamp" H 4500 3000 50  0001 C CNN
F 3 "~" H 4500 3000 50  0001 C CNN
	1    4500 3000
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J2
U 1 1 602D42AB
P 6500 3000
F 0 "J2" H 6450 3250 50  0000 L CNN
F 1 "Conn_01x01" H 6300 3150 50  0000 L CNN
F 2 "Antenna_Clamp_Adapter:Wire_Clamp" H 6500 3000 50  0001 C CNN
F 3 "~" H 6500 3000 50  0001 C CNN
	1    6500 3000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J3
U 1 1 602D5B47
P 5550 3650
F 0 "J3" V 5422 3730 50  0000 L CNN
F 1 "Conn_01x02" V 5513 3730 50  0000 L CNN
F 2 "Antenna_Clamp_Adapter:Amphenol_132255_Edge" H 5550 3650 50  0001 C CNN
F 3 "~" H 5550 3650 50  0001 C CNN
	1    5550 3650
	0    1    1    0   
$EndComp
Wire Wire Line
	5450 3000 5450 3450
Wire Wire Line
	5550 3000 5550 3450
Text Notes 5150 3800 0    50   ~ 0
Amphenol Connector
Wire Wire Line
	4700 3000 5450 3000
Wire Wire Line
	6300 3000 5550 3000
$EndSCHEMATC
