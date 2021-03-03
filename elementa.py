import random
import math

#creates a qubit like structure. The main variable(bitVal) can have a value from 0 to 1
#if it is a zero or one it will always be observed as such, otherwise it will
#be observed as a zero or one randomly with the probability of being observed
#as a one determined, roughly, by the bitVal interpreted as a percentage
class Adambit:
    def __init__(self,inBitVal):
        if inBitVal > 1:
            inBitVal = 1
        if inBitVal < 0:
            inBitVal = 0
            
        self.bitVal = inBitVal

    def observe(self):
        if (self.bitVal > 0) and (self.bitVal < 1):
            if random.random() > self.bitVal:
                return 0
            else:
                return 1
        return self.bitVal

    def getprobamp(self,upordown):
        if upordown == 1:
            return self.bitVal
        else:
            return 1.0 - self.bitVal

#multiplies the probability amps of two Adambits together to get
#the probability amp of each state of the combined two Adambit
#system in a list i.e.
#[amp(00),amp(01),amp(10),amp(11)]
def twotangle(bit1,bit2):
    b1a0 = bit1.getprobamp(0)
    b1a1 = bit1.getprobamp(1)
    b2a0 = bit2.getprobamp(0)
    b2a1 = bit2.getprobamp(1)
    return [b1a0*b2a0,b1a0*b2a1,b1a1*b2a0,b1a1*b2a1]

#turns an int into a list of bits (bools)
def inttobits(num:int,numbits:int):
    retval = [bool(num & (1<<n)) for n in range(numbits)]
    retval.reverse()
    return retval

#generalizes twotangle to an arbitrary number of Adambits
def entangle(bits):
    amps = []
    for abit in bits:
        amps.append([abit.getprobamp(0),abit.getprobamp(1)])
    numbits = len(amps)
    if numbits == 0:
        return []
    retval = []
    for x in range(2**numbits):
        binx = inttobits(x,numbits)
        slotamp = []
        for slot in range(numbits):
            slotamp.append(amps[slot][binx[slot]])
        chainmult = 1
        for y in slotamp:
            chainmult = chainmult * y
        retval.append(chainmult)
    return retval
