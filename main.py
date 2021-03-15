#playback controls: space to pause and play, right for forward, left for backward
#automatically goes from start to finish then back from finish to start, and so on

#I wonder if I should make the rules themselves output three seperate values for
#colorization


import chunkspace
import elementa
import pygame
import random
import png
import sys
import os
from time import time
import multiprocessing as mp

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WINDOW_TITTY = "Chunks in spaaaace!"

FRAME_RATE = 10
VOXELS_X = 100
VOXELS_Y = 100
VOXELS_T = 50

HELP = '''A cellular automata made sweet sweet love to something
a little like a qubit, but not really.
Epilepsy Warning! May cause seizures!

Options:
  1) --save <path>
       saves the cellular automata to pngs in the <path> directory
  2) --load <path>
       plays the pngs in the specified directory like a movie
  3) --no-display
       does not create a window to play the created cellular automata
  4)  No Options!
      creates then plays the cellular automata
'''

#sample rules that works for bools
def conway(vals):
    sumstart = 0
    for i in range(8):
        sumstart += vals[i+1].observe()
    if sumstart == 3:
        return elementa.Adambit(1)
    if (sumstart == 2) and vals[0].observe():
        return elementa.Adambit(1)
    return elementa.Adambit(0)

#sample rules using elementa functions
def tangledup(vals):
    valLen = len(vals) if (len(vals) % 2) == 0 else len(vals) - 1
    oldtangle = None
    for i in range(0,valLen,2):
        if not oldtangle:
            oldtangle = elementa.twotangle(vals[i],vals[i+1])
        else:
            newtangle = elementa.twotangle(vals[i],vals[i+1])
            oldtangle = [og * ng for og,ng in zip(oldtangle,newtangle)]
    return elementa.Adambit(oldtangle[1])

def loadPngArray(path):
    if path[-1] != '/':
        path += '/'
    pings = [pygame.transform.scale(pygame.image.load(path + ping),(SCREEN_WIDTH,SCREEN_HEIGHT))
     for ping in os.listdir(path) if ping[-4:] == '.png']
    return pings

def displayFromPng(pngarray):
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],pygame.RESIZABLE) #set screen dimensions
    pygame.display.set_caption(WINDOW_TITTY) #set screen title
    tock = pygame.time.Clock() #time keeping for animation
    font = pygame.font.SysFont(None,24) #font object for displaying text

    looper = True #main program loop exit flag
    mover = 0 #animator
    movestep = 1 #used to manage playback
    oldstep = 1
    #main program loop
    while looper:
        #event checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #check for quit window event and kills program
                looper = False
            if event.type == pygame.VIDEORESIZE:
                pngarray = [pygame.transform.scale(pickywick,(event.w,event.h)) for pickywick in pngarray]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if movestep == 0:
                        movestep = oldstep
                    else:
                        oldstep = movestep
                        movestep = 0
                elif event.key == pygame.K_RIGHT:
                    movestep = 1
                elif event.key == pygame.K_LEFT:
                    movestep = -1
        screen.fill((255,255,255)) #white background
        screen.blit(pngarray[mover],(0,0))
        framecounter = font.render(str(mover), True, (255,0,0)) #for counting frames
        screen.blit(framecounter,(0,0)) #displays frame number on screen
        pygame.display.flip() #update display
        tock.tick(FRAME_RATE) #sets animation frame rate

        #to index through the temporal dimension of the demiverse
        if mover <= 0:
            movestep = 1
        if mover >= (len(pngarray) - 1):
            movestep = -1
        mover += movestep
    pygame.quit() #yo mama so fat

def displayFromChunks(crapspace):
    #start pygame
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],pygame.RESIZABLE) #set screen dimensions
    pygame.display.set_caption(WINDOW_TITTY) #set screen title
    tock = pygame.time.Clock() #time keeping for animation
    font = pygame.font.SysFont(None,24) #font object for displaying text

    looper = True #main program loop exit flag
    mover = 0 #animator
    movestep = 1 #used to manage playback
    oldstep = 1
    scrSize = (SCREEN_WIDTH,SCREEN_HEIGHT)
    #main program loop
    while looper:
        #event checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #check for quit window event and kills program
                looper = False
            if event.type == pygame.VIDEORESIZE:
                scrSize = (event.w, event.h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if movestep == 0:
                        movestep = oldstep
                    else:
                        oldstep = movestep
                        movestep = 0
                elif event.key == pygame.K_RIGHT:
                    movestep = 1
                elif event.key == pygame.K_LEFT:
                    movestep = -1
        screen.fill((255,255,255)) #white background

        #tiles space
        coordmultX = scrSize[0] / crapspace.wide
        coordmultY = scrSize[1] / crapspace.long
        for i in range(crapspace.wide):
            for j in range(crapspace.long):
                currx = i * coordmultX
                curry = j * coordmultY
                red = int(crapspace.getValue(i-1,j,mover).getprobamp(1) * 255)
                green = int(crapspace.getValue(i,j-1,mover).getprobamp(1) * 255)
                blue = int(crapspace.getValue(i,j,mover-1).getprobamp(1) * 255)
                falseColor = int(crapspace.getValue(i,j,mover).getprobamp(0) * 255)
                bitcol = (red,green,blue) if crapspace.getValue(i,j,mover).observe() else (falseColor,falseColor,falseColor)
                pygame.draw.rect(screen,bitcol,(currx,curry,coordmultX,coordmultY))

        framecounter = font.render(str(mover), True, (255,0,0)) #for counting frames
        screen.blit(framecounter,(0,0)) #displays frame number on screen
        pygame.display.flip() #update display
        tock.tick(FRAME_RATE) #sets animation frame rate

        #to index through the temporal dimension of the demiverse
        if mover <= 0:
            movestep = 1
        if mover >= crapspace.time:
            movestep = -1
        mover += movestep
    pygame.quit() #yo mama so fat

def setGlobalProperties(fromchunks=True):
    global SCREEN_WIDTH
    SCREEN_WIDTH = int(input("Screen Width?: "))
    global SCREEN_HEIGHT
    SCREEN_HEIGHT = int(input("Screen Height?: "))
    if fromchunks:
        xsize = int(input("Pixels per Voxel in Width? :"))
        while xsize <= 0:
            xsize = int(input("WRONG! BAD DOG! BAD BAD BAD!!!\nX Size?: "))
        global VOXELS_X
        VOXELS_X = int(SCREEN_WIDTH / xsize)
        ysize = int(input("Pixels per Voxel in length? :"))
        while ysize <= 0:
            ysize = int(input("WRONG! BAD DOG! BAD BAD BAD!!!\nY Size?: "))
        global VOXELS_Y
        VOXELS_Y = int(SCREEN_HEIGHT / ysize)
        fsize = int(input("Framerate? :"))
        while fsize <= 0:
            fsize = int(input("WRONG! BAD DOG! BAD BAD BAD!!!\nFramerate?: "))
        global FRAME_RATE
        FRAME_RATE = fsize
        tsize = int(input("How Long shall this demiverse last, in seconds?: "))
        while tsize <= 0:
            tsize = int(input("WRONG! BAD DOG! BAD BAD BAD!!!\nT Size?: "))
        tsize = tsize * fsize
        global VOXELS_T
        VOXELS_T = tsize
    print("...loading window...")

def main():
    if '--help' in sys.argv:
        print(HELP)
        exit()
    argind = 0
    for i in range(len(sys.argv)):
        if (sys.argv[i] == '--load') and (len(sys.argv) >= (i+2)):
            if '--no-display' in sys.argv:
                print("...time wasting dumbass...\n\n\n\n\nugh\n\n\n\n\n")
                print("This combination of arguments makes no logical sense, quitting...")
                exit()
            argpath = sys.argv[i+1]
            if argpath[-1] != '/':
                argpath += '/'
            setGlobalProperties(False)
            displayFromPng(loadPngArray(argpath))
            exit()

    setGlobalProperties()
    #setting the initial state to random
    crapspace = chunkspace.ChunkSpace(VOXELS_X,VOXELS_Y,VOXELS_T,elementa.Adambit(0)) #create size of demiverse
    for i in range(crapspace.wide):
        for j in range(crapspace.long):
            crapspace.setValue(i,j,0,elementa.Adambit(random.uniform(0,1)))

    #loading the demiverse according to the rules and inital state
    print ("Loading!!!")
    loadtime = time()
    if '--mp' in sys.argv:
        halfwide = int(crapspace.wide / 2)
        firsthalf = mp.Process(target=crapspace.applyRules,args=(conway,True,(0,halfwide),None,))
        firsthalf.start()
        crapspace.applyRules(conway,True,(halfwide,crapspace.wide),None)
        firsthalf.join()
    else:
        crapspace.applyRules(conway,True,None,None)
    loadtime = time() - loadtime
    print("\nAll Loaded Up. And it only took", loadtime, "seconds!\n...jesus...")

    for i in range(len(sys.argv)):
        if (sys.argv[i] == '--save') and (len(sys.argv) >= (i+2)):
            argpath = sys.argv[i+1]
            if argpath[-1] != '/':
                argpath += '/'
            print ("Saving to PNG")
            crapspace.saveToPics(argpath)
            print("\nDone Saving")

    #displays the created demiverse
    if '--no-display' in sys.argv:
        exit()
    else:
        displayFromChunks(crapspace)

if __name__ == "__main__":
    main()
