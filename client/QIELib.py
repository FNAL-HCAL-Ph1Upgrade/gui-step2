from client import webBus

b = webBus("pi5",0) #can add "pi5,0" so won't print send/receive messages

def openChannel():
  b.write(0x72,[0x02])
  b.write(0x74,[0x02])
  b.sendBatch()

#Library of tables, functions, and classes for working with QIE11 test stands

#MUX slave addresses (slave i2c addresses)
MUXs = {
    "fanout" : 0x72,
    "ngccm" : {
                "u10" : 0x74,
                "u18" : 0x70
                },
    "bridge" : [0x19, 0x1a, 0x1b, 0x1c]
        }
#Register addresses
REGs = {
    "qie0" : 0x30,
    "qie1" : 0x31,
    "iscSelect" : 0x11,
    "vttx" : 0x7E,
    "igloo" : 0x09,
    "ID" : 0x50,
    "temp" : 0x40
        }
# Simplify your life today with RMi2c and QIEi2c. Boom dog.

RMi2c = {
    0 : 0x02,
    1 : 0x20,
    2 : 0x10,
    3 : 0x01
        }

QIEi2c = {
    0 : 0x19,
    1 : 0x1a,
    2 : 0x1b,
    3 : 0x1c
        }

shiftRegisterAddresses = [0x30, 0x31]

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
        "slots" : [2,3,4,5],
        "sipm" : 1,
        "slotGroup" : 2,
        "sipmGroup" : 1
        },
    3 : {
        "slots" : [7,8,9,10],
        "sipm" : 6,
        "slotGroup" : 4,
        "sipmGroup" : 3
        },
    2 : {
        "slots" : [18,19,20,21],
        "sipm" : 17,
        "slotGroup" : 7,
        "sipmGroup" : 6
        },
    1 : {
        "slots" : [23,24,25,26],
        "sipm" : 22,
        "slotGroup" : 9,
        "sipmGroup" : 8
        }
      }

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
