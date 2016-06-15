import json

print "\n"
fileName = "0x000000ea9dec_raw.json"
inputFile = open(fileName,"r")
qieCard=json.load(inputFile)
print qieCard["tester"]
print qieCard["humidity"]
print qieCard["temperature"]
print "\n"
