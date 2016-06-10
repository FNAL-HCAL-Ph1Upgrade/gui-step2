import json

print "\n"
for i in ("0x19","0x1a","0x1b","0x1c"):
	fileName = "shogan_"+i+"_raw.json"
	inputFile = open(fileName,"r")
	qieCard=json.load(inputFile)
	print qieCard["tester"]
	print qieCard["humidity"]
	print qieCard["temperature"]
	print "\n"
