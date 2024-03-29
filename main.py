##conway
##tangledup
##gravity
##abitgravity
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

def gravity(vals):
    summer = 0
    g = 4
    for val in vals:
        summer += val.observe()
    if summer > g:
        return elementa.Adambit(1)
    else:
        return elementa.Adambit(0)

def abitgravity(vals):
    summer = 0
    g = 2.5
    for val in vals:
        summer += val.getprobamp(1)
    if summer > g:
        return elementa.Adambit(summer / len(vals))
    else:
        return elementa.Adambit(summer / (len(vals) * 2))

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
                red = int(crapspace.getValue(i,j,mover-1).getprobamp(1) * 255)
                green = int(crapspace.getValue(i,j,mover).getprobamp(1) * 255)
                blue = int(crapspace.getValue(i,j,mover+1).getprobamp(1) * 255)
                bitcol = (red,green,blue) if crapspace.getValue(i,j,mover).observe() else (0,0,0)
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

def loaderScreen():
    if pygame.get_sdl_version() < (2,0,0):
        print("Loading Window requires SDL version 2.0 or greater")
        return False
    screendims = (500,500)
    pygame.init()
    screen = pygame.display.set_mode(screendims)
    pygame.display.set_caption("Set Demiverse Properties")
    ticker = pygame.time.Clock()
    editfont = pygame.font.SysFont(None,30)
    displayfont = pygame.font.SysFont(None,32)
    pygame.key.start_text_input()
    cursor  = ['|',60] #(cursor char,blinkrate)
    submitButton = displayfont.render("Submit",True,(0,0,0))
    submitBound = submitButton.get_rect()
    submitBound.y = screendims[1] - (submitBound.h + 10)
    submitBound.x = int(screendims[0] / 2) - int(submitBound.w / 2)
    blinker = 1
    blinkflag = False
    preInputText = ""
    postInputText = ""
    errorText = ""
    errorFlag = False
    errortime = 3
    errorframes = 0
    prompts = ["Screen Height (px) ",
    "Screen Width (px)  ",
    "Chunk Height (px)  ",
    "Chunk Width (px)   ",
    "Framerate (fps)     ",
    "Duration (sec)       "]
    flatPrompts = ["screen_height","screen_width","chunk_height","chunk_width","framerate","duration"]
    promptLabels = []

    for i, prompt in enumerate(prompts):
        promptLabel = displayfont.render(prompt,True,(0,0,0))
        inputx = promptLabel.get_width() + 5
        inputy = int((i * screendims[1]) / len(prompts)) + 10
        inputw = screendims[0] - inputx - 5
        inputh = promptLabel.get_height()
        promptLabels.append([promptLabel,pygame.Rect(inputx,inputy,inputw,inputh),""])

    focus_i = 0
    focus = promptLabels[focus_i][1].inflate(-5,-5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_BACKSPACE):
                if len(preInputText) > 0:
                    preInputText = preInputText[:-1]
                continue
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_DELETE):
                if len(postInputText) > 0:
                    postInputText = postInputText[1:]
                continue
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_TAB):
                promptLabels[focus_i][2] = preInputText + postInputText
                focus_i = 0 if focus_i >= (len(promptLabels) - 1) else focus_i + 1
                focus = promptLabels[focus_i][1].inflate(-5,-5)
                preInputText = promptLabels[focus_i][2]
                postInputText = ""
                continue
            if (event.type == pygame.MOUSEBUTTONUP) and (submitBound.collidepoint(event.pos)):
                promptLabels[focus_i][2] = preInputText + postInputText
                try:
                    retval = []
                    for i, label in enumerate(promptLabels):
                        retval.append((flatPrompts[i],int(label[2])))
                    retval = dict(retval)
                    pygame.quit()
                    return retval
                except:
                    errorText = "Not all values are numeric, try again"
                    errorFlag = True
                    errorframes = errortime * 60
            if event.type == pygame.MOUSEBUTTONUP:
                for i,label in enumerate(promptLabels):
                    if label[1].collidepoint(event.pos):
                        promptLabels[focus_i][2] = preInputText + postInputText
                        focus_i = i
                        focus = promptLabels[focus_i][1].inflate(-5,-5)
                        preInputText = promptLabels[focus_i][2]
                        postInputText = ""
                continue
            if (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_LEFT) or event.key == pygame.K_RIGHT):
                if event.key == pygame.K_RIGHT:
                    if len(postInputText) > 0:
                        preInputText = preInputText + postInputText[0]
                        postInputText = postInputText[1:]
                else:
                    if len(preInputText) > 0:
                        postInputText = preInputText[-1] + postInputText
                        preInputText = preInputText[:-1]
                continue
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_HOME):
                postInputText = preInputText + postInputText
                preInputText = ""
                continue
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_END):
                preInputText = preInputText + postInputText
                postInputText = ""
                continue
            if event.type == pygame.TEXTINPUT:
                preInputText += event.text

        screen.fill((100,125,150))
        for promptLabel in promptLabels:
            screen.blit(promptLabel[0], (0,promptLabel[1][1]))
            pygame.draw.rect(screen,(0,0,0),promptLabel[1].inflate(4,4))
            pygame.draw.rect(screen,(255,255,255),promptLabel[1])

        pygame.draw.rect(screen,(0,0,0),submitBound.inflate(5,5))
        pygame.draw.rect(screen,(200,200,200),submitBound)
        screen.blit(submitButton,submitBound)

        if (cursor[1] % blinker) == 0:
                blinkflag = not blinkflag

        preEditText = editfont.render(preInputText,True,(0,0,0))
        postEditText = editfont.render(postInputText,True,(0,0,0))
        for i,label in enumerate(promptLabels):
            if focus_i == i:
                screen.blit(preEditText,focus)
                if blinkflag:
                    cursorText = editfont.render(cursor[0],True,(0,0,0))
                    screen.blit(cursorText,(preEditText.get_rect().right+focus.x-2,focus.y))
                screen.blit(postEditText,(preEditText.get_rect().right+focus.x,focus.y))
            else:
                screen.blit(editfont.render(label[2],True,(0,0,0)),label[1].inflate(-5,-5))
        if errorFlag:
            errorDisplay = displayfont.render(errorText,True,(255,0,0))
            errorRect = errorDisplay.get_rect()
            errorRect.x = 0
            errorRect.y = screendims[1] - errorRect.h
            pygame.draw.rect(screen,(255,240,240),errorRect)
            screen.blit(errorDisplay,errorRect)
        errorframes = 0 if errorframes <= 0 else errorframes - 1
        errorFlag = errorframes != 0
        pygame.display.flip()
        blinker = blinker + 1 if blinker <= cursor[1] else 1
        ticker.tick(60)

    pygame.quit()
    return False

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

def setGlobalsFromDict(indick):
    global SCREEN_WIDTH, SCREEN_HEIGHT, VOXELS_T, VOXELS_X, VOXELS_Y, FRAME_RATE
    SCREEN_WIDTH = indick["screen_width"]
    SCREEN_HEIGHT = indick["screen_height"]
    VOXELS_X = int(SCREEN_WIDTH / indick["chunk_width"])
    VOXELS_Y = int(SCREEN_HEIGHT / indick["chunk_height"])
    FRAME_RATE = indick["framerate"]
    VOXELS_T = indick["duration"] * FRAME_RATE

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

    setGlobalsFromDict(loaderScreen())
    thisfile = open('main.py', 'r')
    rulefuncs = []
    for line in thisfile.readlines():
        if (len(line) > 2) and (line[:2] == "##"):
            rulefuncs.append(line[2:-1])
    thisfile.close()
    rulefunc = None
    while not (rulefunc in rulefuncs):
        print("Pick Rule to Use:")
        for possible in rulefuncs:
            print(' ', possible)
        rulefunc = input("Choose: ")
    rulefunc = eval(rulefunc)

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
        firsthalf = mp.Process(target=crapspace.applyRules,args=(rulefunc,True,(0,halfwide),None,))
        firsthalf.start()
        crapspace.applyRules(rulefunc,True,(halfwide,crapspace.wide),None)
        firsthalf.join()
    else:
        crapspace.applyRules(rulefunc,True,None,None)
    loadtime = time() - loadtime
    print("\nAll Loaded Up. And it only took", loadtime, "seconds!")

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
