#!/usr/bin/python
#
#QIELib.py
#Library of tables, functions, and classes for working with QIE11 test stands

#Bit to write to mux for given twisted pair i2c
i2cGroups = {
    1 : 0x04,
    2 : 0x02,
    3 : 0x01,
    4 : 0x20,
    5 : 0x10,
    6 : 0x20,
    7 : 0x10,
    8 : 0x02,
    9 : 0x01
            }
RMs = {
    4 : {
        "slots" : ["J2", "J3", "J4", "J5"],
        "sipmC" : "J1",
        "slotGroup" : 2,
        "sipmGroup" : 1
        },
    3 : {
        "slots" : ["J7", "J8", "J9", "J10"],
        "sipmC" : "J6",
        "slotGroup" : 4,
        "sipmGroup" : 3
        },
    2 : {
        "slots" : ["J18", "J19", "J20", "J21"],
        "sipmC" : "J17",
        "slotGroup" : 7,
        "sipmGroup" : 6
        },
    1 : {
        "slots" : ["J23", "J24", "J25", "J26"],
        "sipmC" : "J22",
        "slotGroup" : 9,
        "sipmGroup" : 8
        }
      }

#For higher J, subtract 5
JSlots = {
    1  : 0x18,
    2  : 0x19,
    3  : 0x1A,
    4  : 0x1B,
    5  : 0x1C,
    6  : 0x18,
    7  : 0x19,
    8  : 0x1A,
    9  : 0x1B,
    10 : 0x1C,
    17 : 0x18,
    18 : 0x19,
    19 : 0x1A,
    20 : 0x1B,
    21 : 0x1C,
    22 : 0x18,
    23 : 0x19,
    24 : 0x1A,
    25 : 0x1B,
    26 : 0x1C
         }

serialShiftRegisterBits = {
    "LVDS/SLVS" : [0],
    "P0, P1" : [1, 2],
    "DiscOn" : [3],
    "TGain" : [4],
    "TimingThresholdDAC" : [5,6,7,8,9,10,11,12],
    "TimingIref" : [13,14,15],
    "PedastalDAC" : [16,17,18,19,20,21],
    "CapID0pedastal" : [22,23,24,25],
    "CapID1pedastal" : [26,27,28,29],
    "CapID2pedastal" : [30,31,32,33],
    "CapID3pedastal" : [34, 35, 36, 37],
    "FixRange" : [38],
    "RangeSet" : [39, 30],
    "ChargeInjectDAC" : [41, 42, 43],
    "Gsel" : [44, 45, 46, 47, 48],
    "Idcset" : [49, 50, 51, 52, 53],
    "CkOutEn" : [54],
    "TDCmode" : [55],
    "Hsel" : [56],
    "PhaseDelay" : [57, 58, 59, 60, 61, 62, 63]
}
