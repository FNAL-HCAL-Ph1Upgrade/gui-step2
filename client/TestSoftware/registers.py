#registers.py

registers = {
    "ID_string" :{
        "address" : 0x00,
        "size" : 32,
        "RW" : 0
        },
    "ID_string_cont" :{
        "address" : 0x01,
        "size" : 32,
        "RW" : 0
        },
    "FW_Version" :{
        "address" : 0x04,
        "size" : 32,
        "RW" : 0
        },
    "Ones" :{
        "address" : 0x08,
        "size" : 32,
        "RW" : 0
        },
    "Zeroes" :{
        "address" : 0x09,
        "size" : 32,
        "RW" : 0
        },
    "OnesZeroes" :{
        "address" : 0x0A,
        "size" : 32,
        "RW" : 0
        },
    "Scratch" :{
        "address" : 0x0B,
        "size" : 32,
        "RW" : 1
        },
    "Status" :{
        "address" : 0x10,
        "size" : 32,
        "RW" : 0
        },
    "I2C_SELECT" :{
        "address" : 0x11,
        "size" : 8,
        "RW" : 1
        },
    "Clock_Counter" :{
        "address" : 0x12,
        "size" : 32,
        "RW" : 0
        },
    "RES_QIE_Counter" :{
        "address" : 0x13,
        "size" : 32,
        "RW" : 0
        },
    "WTE_Counter" :{
        "address" : 0x14,
        "size" : 32,
        "RW" : 0
        },
    "BkPln_Spare_1_Counter" :{
        "address" : 0x15,
        "size" : 32,
        "RW" : 0
        },
    "BkPln_Spare_2_Counter" :{
        "address" : 0x16,
        "size" : 32,
        "RW" : 0
        },
    "BkPln_Spare_3_Counter" :{
        "address" : 0x17,
        "size" : 32,
        "RW" : 0
        },
    "igloo2_FPGA_Control" :{
        "address" : 0x22,
        "size" : 11,
        "RW" : 1
        },
    "ControlReg" :{
        "address" : 0x2A,
        "size" : 32,
        "RW" : 1
        },
    "orbit_histo[167:144]" :{
        "address" : 0x2B,
        "size" : 24,
        "RW" : 0
        },
    "orbit_histo[143:120]" :{
        "address" : 0x2C,
        "size" : 24,
        "RW" : 0
        },
    "orbit_histo[119:96]" :{
        "address" : 0x2D,
        "size" : 24,
        "RW" : 0
        },
    "orbit_histo[95:72]" :{
        "address" : 0x2E,
        "size" : 24,
        "RW" : 0
        },
    "orbit_histo[71:48]" :{
        "address" : 0x2F,
        "size" : 24,
        "RW" : 0
        },
    "orbit_histo[47:24]" :{
        "address" : 0x30,
        "size" : 24,
        "RW" : 0
        },
    "orbit_histo[23:0]" :{
        "address" : 0x31,
        "size" : 24,
        "RW" : 0
        },
    "QIE_Daisy_Chain_0" :{
        "address" : 0x30,
        "size" : 384,
        "RW" : 1
        },
    "QIE_Daisy_Chain_1" :{
        "address" : 0x31,
        "size" : 384,
        "RW" : 1
        },
    "QIE_Daisy_Chain_2" :{
        "address" : 0x32,
        "size" : 384,
        "RW" : 1
        },
    "QIE_Daisy_Chain_3" :{
        "address" : 0x33,
        "size" : 384,
        "RW" : 1
        },
    "Thermometer_One_Wire" :{
        "address" : 0x40,
        "size" : 8,
        "RW" : 1
        }
}
