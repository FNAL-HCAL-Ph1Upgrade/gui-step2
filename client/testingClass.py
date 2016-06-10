from qieCardClass import qieCard
import pickle
import json

card1 = qieCard()
print card1.temperature
card1.temperature = 25
print card1.temperature
f = open("testFile", 'w')

def jdefault(o):
	return o.__dict__


print(json.dump(card1, f, default=jdefault))
