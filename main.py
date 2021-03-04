#playback controls: space to pause and play, right for forward, left for backward
#automatically goes from start to finish then back from finish to start, and so on


import chunkspace
import elementa
import pygame
import random
import png
import sys

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

FRAME_RATE = 30
VOXELS_X = 100 #int(SCREEN_WIDTH / 5)
VOXELS_Y = 100 #int(SCREEN_HEIGHT / 5)
VOXELS_T = 20

ERROR = '''ERROR! Valid command line arguments are:
   1)None, obviously
   2)--save <path>
     for saving the demiverse as a bunch of pngs
   3)--load <path>
     not implemented, but will be for loading from a bunch of pngs
   4)--no-display
     which you would add to the END of any argument list if you don't want to
     pygame it up'''

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

def displayFromChunks(crapspace):
    #start pygame
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT]) #set screen dimensions
    pygame.display.set_caption('Chunks in spaaaace!') #set screen title
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
        if mover < 0:
            movestep = 1
        if mover >= crapspace.time:
            movestep = -1
        mover += movestep
    pygame.quit() #yo mama so fat

def main():
    crapspace = chunkspace.ChunkSpace(VOXELS_X,VOXELS_Y,VOXELS_T,elementa.Adambit(0)) #create size of demiverse

    #setting the initial state to random
    for i in range(crapspace.wide):
        for j in range(crapspace.long):
            crapspace.setValue(i,j,0,elementa.Adambit(random.uniform(0,1)))

    #loading the demiverse according to the rules and inital state
    print ("Loading!!!")
    crapspace.applyRules(conway,1,True)
    print("\nDone Been Loaded!!! Yeehaw!!! *shoots pistols in air* Yipee Kai Yay Motherfucker!!!")

    #probably should implement this better at some later date
    #but it handles command line arguments
    sys.argv.remove('main.py')
    if len(sys.argv) <= 0:
        displayFromChunks(crapspace)
    elif len(sys.argv) > 1:
        if sys.argv[0] == "--save":
            path = sys.argv[1]
            if path[-1] != '/':
                path += '/'
            crapspace.saveToPics(path)
            if (len(sys.argv) > 2) and (sys.argv[2] == "--no-display"):
                exit()
        elif sys.argv == "--load":
            print("Loading from file not implemented yet!")
            exit()
        else:
            print(ERROR)
            exit()
    elif len(sys.argv) == 1:
        if sys.argv[0] == "--no-display":
            exit()
    else:
        print(ERROR)

    displayFromChunks(crapspace)

if __name__ == "__main__":
    main()
