#playback controls: space to pause and play, right for forward, left for backward
#automatically goes from start to finish then back from finish to start, and so on


import chunkspace
import elementa
import pygame
import random
import png
import sys
import os

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WINDOW_TITTY = "Chunks in spaaaace!"

FRAME_RATE = 30
VOXELS_X = 50 #int(SCREEN_WIDTH / 5)
VOXELS_Y = 50 #int(SCREEN_HEIGHT / 5)
VOXELS_T = 10

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
    tangles = elementa.entangle(vals)
    return elementa.Adambit(tangles[0])

def loadPngArray(path):
    if path[-1] != '/':
        path += '/'
    pings = [pygame.transform.scale(pygame.image.load(path + ping),(SCREEN_WIDTH,SCREEN_HEIGHT))
     for ping in os.listdir(path) if ping[-4:] == '.png']
    return pings

def displayFromPng(pngarray):
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT]) #set screen dimensions
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
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT]) #set screen dimensions
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
        coordmultX = SCREEN_WIDTH / crapspace.wide
        coordmultY = SCREEN_HEIGHT / crapspace.long
        for i in range(crapspace.wide):
            for j in range(crapspace.long):
                currx = i * coordmultX
                curry = j * coordmultY
                red = int(crapspace.getValue(i,j,mover).getprobamp(1) * 255)
                green = int(crapspace.getValue(i,j,mover-1).getprobamp(1) * 255)
                blue = int(crapspace.getValue(i,j,mover+1).getprobamp(1) * 255)
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
            displayFromPng(loadPngArray(argpath))
            exit()

    #setting the initial state to random
    crapspace = chunkspace.ChunkSpace(VOXELS_X,VOXELS_Y,VOXELS_T,elementa.Adambit(0)) #create size of demiverse
    for i in range(crapspace.wide):
        for j in range(crapspace.long):
            crapspace.setValue(i,j,0,elementa.Adambit(random.uniform(0,1)))

    #loading the demiverse according to the rules and inital state
    print ("Loading!!!")
    crapspace.applyRules(conway,1,True)
    print("\nDone Been Loaded!!! Yeehaw!!! *shoots pistols in air* Yipee Kai Yay Motherfucker!!!")

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
