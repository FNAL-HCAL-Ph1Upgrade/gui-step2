import sys
sys.path.append("../")
from client import webBus

pi = sys.args[1]
bus = webBus(pi,0)


