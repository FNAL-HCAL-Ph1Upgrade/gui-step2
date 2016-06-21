class Test:
#   def __init__(self, bus, address, logfile, iterations = 1):
    def __init__(self,bus,address,iterations=1):
        self.bus = bus
        self.address = address
#        self.logstream = logstream
        self.iterations = iterations

    def run(self):
        passes = 0
        for i in xrange(100):
            if self.testBody() == True: passes += 1
	fails = 100 - passes
        return (passes, fails)

#   def log(self, message):
#       logprint(message, file=self.logfile)

    def testBody(self):
        return True


