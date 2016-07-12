<<<<<<< HEAD
=======
class ADCConverter:
    # Bitmasks for 8-bit ADC input

    expMask = 192
    manMask = 63
    baseSensitivity = 3.1
    # Base charges for each subrange
    # Use array for which 0 ADC = 0 fC input charge
    inputCharge = [
        -1.6, 48.4, 172.4, 433.4, 606.4,
        517, 915, 1910, 3990, 5380,
        4780, 7960, 15900, 32600, 43700,
        38900, 64300, 128000, 261000, 350000
    ]

    #Defines the size of the ADC mantissa subranges
    adcBase = [0, 16, 36, 57, 64]

    # A class to convert ADC to fC
    fc = {}

    def __init__(self):
        # Loop over exponents, 0 - 3
        for exp in xrange(0, 4):
            # Loop over mantissas, 0 - 63
            for man in xrange(0, 64):
                subrange = -1
                # Find which subrange the mantissa is in
                for i in xrange(0, 4):
                    if man >= self.adcBase[i] and man < self.adcBase[i + 1]:
                        subrange = i

                if subrange == -1:
                    print 'Something has gone horribly wrong!'

                # Sensitivity = 3.1 * 8^exp * 2^subrange
                sensitivity = self.baseSensitivity * 8.0**float(exp) * 2.0**subrange
                # Add sensitivity * (location in subrange) to base charge
                #fc[exp * 64 + man] = (inputCharge[exp * 5 + subrange] + ((man - adcBase[subrange])) * sensitivity) / gain;
                self.fc[exp * 64 + man] = self.inputCharge[exp * 5 + subrange] + ((man - self.adcBase[subrange]) + .5) * sensitivity

    def linearize(self, adc):
        return self.fc[adc]


myadc = ADCConverter()
for i in xrange(255):
    print '%d ADC: ' %i+str(myadc.linearize(i))
>>>>>>> 18be54736405b701a54c06e1462b41baf7577eac
