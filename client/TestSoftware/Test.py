class Test:
    def __init__(self,bus,address,iterations=1):
        self.bus = bus
        self.address = address
        self.iterations = iterations

    def run(self):
        passes = 0
        for i in xrange(self.iterations):
            if self.testBody() == True: passes += 1
	fails = self.iterations - passes
        return (passes, fails)

    def testBody(self):
        return True
