import elementa
import png

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
    def locality(self,x,y,t,pastOnly):
        coords = [
        (x-1,y-1,t-1),
        (x-1,y,t-1),
        (x-1,y+1,t-1),
        (x,y-1,t-1),
        (x,y,t-1),
        (x,y+1,t-1),
        (x+1,y-1,t-1),
        (x+1,y,t-1),
        (x+1,y+1,t-1)]

        if pastOnly:
            return coords
        coords += [
        (x-1,y-1,t),
        (x-1,y,t),
        (x-1,y+1,t),
        (x,y-1,t),
        (x,y,t),
        (x,y+1,t),
        (x+1,y-1,t),
        (x+1,y,t),
        (x+1,y+1,t),
        (x-1,y-1,t+1),
        (x-1,y,t+1),
        (x-1,y+1,t+1),
        (x,y-1,t+1),
        (x,y,t+1),
        (x,y+1,t+1),
        (x+1,y-1,t+1),
        (x+1,y,t+1),
        (x+1,y+1,t+1)]

        return coords
    def applyRules(self,rules,pastOnly,xsub,ysub):
        retval = []

        print ('┌', end='',flush='True') #load meter
        for t in range(self.time - 1):
            print ('─', end='',flush='True') #load meter
        print ('┐\n ',end='',flush='True') #load meter

        if xsub:
            if (xsub[0] < 0) or (xsub[1] >= self.wide):
                xsub = (0,self.wide)
        else:
            xsub = (0,self.wide)
        if ysub:
            if (ysub[0] < 0) or (ysub[1] >= self.long):
                ysub = (0,self.long)
        else:
            ysub = (0,self.long)

        t = 1
        while t < self.time:
            print ('█', end='',flush='True') #load meter
            for x in range(xsub[0],xsub[1]):
                for y in range(ysub[0],ysub[1]):
                    localCoords = self.locality(x,y,t,pastOnly)
                    localValues = [self.getValue(acord[0],acord[1],acord[2]) for acord in localCoords]
                    self.spacemat[x][y][t] = rules(localValues)
            t += 1

    def saveToPics(self,path):
        for t in range(self.time):
            print ('█', end='',flush='True') #load meter
            pngArray = []
            for y in range(self.long):
                pngArray.append([])
                for x in range(self.wide):
                    if self.getValue(x,y,t).observe():
                        pngArray[y].append(int(self.getValue(x,y,t).getprobamp(1) * 255))
                        pngArray[y].append(int(self.getValue(x,y,t-1).getprobamp(1) * 255))
                        pngArray[y].append(int(self.getValue(x,y,t+1).getprobamp(1) * 255))
                    else:
                        pngArray[y].append(int(self.getValue(x,y,t).getprobamp(0) * 255))
                        pngArray[y].append(int(self.getValue(x,y,t).getprobamp(0) * 255))
                        pngArray[y].append(int(self.getValue(x,y,t).getprobamp(0) * 255))
            png.from_array(pngArray,'RGB').save(path + str(t) + ".png")
