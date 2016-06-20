
# Open Channel to RM
def openChannel(rmSlot):
    b = webBus("pi5",0)
    if rmSlot in [3,4]:
        # Open channel to ngCCM for RM 3,4: J1 - J10
        b.write(0x72,[0x02])
        if (rmSlot == 3):
	   b.write(0x74,[0x20])
	else:
	   b.write(0x74,[0x02])	
    elif rmSlot in [1,2]:
        # Open channel to ngCCM for RM 1,2: J17 - J26
        b.write(0x72,[0x01])
	if (rmSlot == 2):
	   b.write(0x74,[0x10])
	else:
	   b.write(0x74,[0x01])
	

import openChannel

for rm in (1,2,3,4):
	openChannel(rm)
	for card in (0x19,0x1a,0x1b,0x1c):
		stuff

	
