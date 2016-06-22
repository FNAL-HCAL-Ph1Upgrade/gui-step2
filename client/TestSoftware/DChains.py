#DChains.py

from DaisyChain import DaisyChain
from client import webBus
from helpers import *
from optparse import OptionParser

class DChains:
    def __init__(self, address, bus):
        self.bus = bus
        self.chains = []
        self.address = address
    def read(self):
        for register in [0x30, 0x31]:
            self.chains.append(DaisyChain(readBinaryRegister(self.bus, self.address, register, 48)))
    def __str__(self):
        ret = ""
        for c in self.chains:
            ret += str(c)
        return ret
    def __getitem__(self, i):
        return self.Chains[i/6][i % 6]
    def write(self):
        for i in range(2):
            register = [0x30, 0x31][i]
            writeToRegister(self.bus, self.address, register, getBytesFromBits(self.chains[i].flatten()))
