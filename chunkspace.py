import elementa

class ChunkSpace:
    def __init__(self,w,l,t,fillValue):
        self.spacemat = [[[fillValue for w0 in range(t)] for l0 in range(l)] for t0 in range(w)]
        self.wide = w
        self.long = l
        self.time = t
        self.fill = fillValue
    def setValue(self,x,y,t,v):
        if (x < self.wide) and ((y < self.long) and (t < self.time)):
            if (x >= 0) and ((y >= 0) and (t >= 0)):
                self.spacemat[x][y][t] = v
                return True
        return False
    def getValue(self,x,y,t):
        if (x < self.wide) and ((y < self.long) and (t < self.time)):
            if (x >= 0) and ((y >= 0) and (t >= 0)):
                return self.spacemat[x][y][t]
        return self.fill
    def locality(self,x,y,t,n,pastOnly):
        coords = []

        if pastOnly:
            for i in range(3 * n):
                for j in range(3 * n):
                    coords.append([x+(j-n),y+(i-n),t-n])
            return coords

        for i in range(3 * n):
            for j in range(3 * n):
                for k in range(3 * n):
                    coords.append([x+(k-n),y+(j-n),t+(i-n)])
        return coords
    def applyRules(self,rules,n,pastOnly=False):
        retval = []

        print ('┌', end='',flush='True') #load meter
        for t in range(self.time - 1):
            print ('─', end='',flush='True') #load meter
        print ('┐\n ',end='',flush='True') #load meter

        t = 1
        while t < self.time:
            print ('█', end='',flush='True') #load meter
            for x in range(self.wide):
                for y in range(self.long):
                    localCoords = self.locality(x,y,t,n,pastOnly)
                    localValues = [self.getValue(acord[0],acord[1],acord[2]) for acord in localCoords]
                    self.spacemat[x][y][t] = rules(localValues)
            t += 1
