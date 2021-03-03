import chunkspace
import elementa
import pygame
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

FRAME_RATE = 10
VOXELS_X = int(SCREEN_WIDTH / 5)
VOXELS_Y = int(SCREEN_HEIGHT / 5)
VOXELS_T = 100

def conway(vals):
    sumstart = 0
    for i in range(8):
        sumstart += vals[i+1].observe()
    if sumstart == 3:
        return elementa.Adambit(1)
    if (sumstart == 2) and vals[0].observe():
        return elementa.Adambit(1)
    return elementa.Adambit(0)

def tangledup(vals):
    tangles = elementa.entangle([vals[0],vals[1],vals[2],vals[3]])
    return elementa.Adambit(tangles[0])

def main():
    pygame.init() #start pygame
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT]) #set screen dimensions
    pygame.display.set_caption('Chunks in spaaaace!') #set screen title
    crapspace = chunkspace.ChunkSpace(VOXELS_X,VOXELS_Y,VOXELS_T,elementa.Adambit(0)) #create size of demiverse
    tock = pygame.time.Clock() #time keeping for animation
    font = pygame.font.SysFont(None,24) #font object for displaying text

    #setting the initial state
    for i in range(crapspace.wide):
        for j in range(crapspace.long):
            crapspace.setValue(i,j,0,elementa.Adambit(random.uniform(0,1)))

    #loading the demiverse according to the rules and inital state
    print ("Loading!!!")
    crapspace.applyRules(tangledup,1)
    print("\nDone Been Loaded!!! Yeehaw!!! *shoots pistols in air* Yipee Kai Yay Motherfucker!!!")

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
                bitcol = (200,200,200) if crapspace.getValue(i,j,mover).observe() else (0,0,0)
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

if __name__ == "__main__":
    main()
