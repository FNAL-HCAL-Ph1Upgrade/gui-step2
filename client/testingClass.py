from qieCardClass import qieCard
import pickle

card1 = qieCard()
print card1.temperature
card1.temperature = 25
print card1.temperature
f = open("testFile", 'w')
pickle.dump(card1,f)
