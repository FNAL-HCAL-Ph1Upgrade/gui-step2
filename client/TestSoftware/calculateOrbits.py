import helpers as t
import time


def control_reg_orbit_histo(bus,slot,delay):
    bus.write(slot,[0x18,2,0,0,0])
    bus.sendBatch()
    bus.write(slot,[0x18,1,0,0,0])
    bus.sendBatch()
    time.sleep(delay)
    bus.write(slot,[0x18,0,0,0,0])
    bus.sendBatch()
    # runBridgeTests([rm],t.getSlotList(rm,slot),range(16,24),0)
    bus.write(slot,[0x1D])
    bus.read(slot,3)
    message = bus.sendBatch()
    message = message[-1][2:]
    message = t.reverseBytes(message)
    value = t.getValue(message)
    return value

def calcOrbs(bus,slot,seconds,verbose=0):
    a = control_reg_orbit_histo(bus,slot,0)
    b = control_reg_orbit_histo(bus,slot,seconds)

    orbitTime1 = 88.924 # microseconds
    # Frequency = 11kHz... this corresponds to b

    bunches = 3564 # total number of bunches
    # spacing = 25.0 * 10**-3 # spacing in microseconds... 25ns
    bunchFrequency = 40.07897 # MHz
    orbitFrequency = 11.2455 # kHz
    spacing = 1/bunchFrequency # 24.95 ns
    orbitTime2 = bunches * spacing # 88.924 microseconds
    orbitTime3 = (1/11.2455) * 10**3 # 88.924 microseconds

    orbits = float(b - a)
    orbitsPerSec = orbits/seconds
    if (int(orbitsPerSec) == 0):
	print 'ERROR: Division by zero. Continuing...'
        return False  # this avoids a div by zero error
    else:
    	secondsPerOribt = 1/orbitsPerSec # seconds per orbit
    orbitTimeMeasured = secondsPerOribt * 10**6 # microseconds per orbit

    percErr = 100 * abs(orbitTimeMeasured-orbitTime1)/orbitTime1

    if verbose:
        print 'num orbits a        = '+str(a)
        print 'num orbits b        = '+str(b)
        print 'orbits diff = b - a = '+str(orbits)
        print 'time delay (s)      = '+str(seconds)
        print 'orbits per second   = '+str(orbitsPerSec)
        print 'seconds per orbit   = '+str(secondsPerOribt)
    
    print 'theoretical orbit time (microseconds) = '+str(orbitTime1)
    # print orbitTime2
    print 'measured orbit time (microseconds) = '+str(orbitTimeMeasured)
    print 'percent error           =  '+str(percErr)+' % error'

    if percErr < 0.5:
	print 'Passes!\n'
        return True
    else:
	print 'Fails...\n'
        return False
