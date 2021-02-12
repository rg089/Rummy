import pygame, sys, random
from pygame.locals import *
from Indian_Rummy import *

d={"c":0,"d":1,"h":2,"s":3}
suits=["c","d","h","s"]

BLACK =         (  0,   0,   0)
BRIGHTBLUE =    (  0,  50, 255)
GREEN =         (  0, 204,   0)
BLUE=           (  0,   0, 255)
RED=            (255,   0,   0)
ORANGE=         (255,  83,  10)

pygame.init()

#s=input("Enter your name - ")
s="r"

DISPLAYSURF=pygame.display.set_mode((1130,700))
pygame.display.set_caption("Rummy Layout")

pygame.mixer.music.load(r'back.mp3')
pygame.mixer.music.play(-1, 0.0)

cardImg1=pygame.image.load(r"back.png")
jokericon=pygame.image.load(r"Joker2.png")
jokericon=pygame.transform.rotate(jokericon,-45)

fontObj = pygame.font.SysFont('segoescript', 16)
textSurfaceObj = fontObj.render('Discard Pile', True, RED)

fontObj5 = pygame.font.SysFont('segoescript', 22)
textSurfaceObj5 = fontObj5.render('First Life', True, ORANGE)

fontObj8 = pygame.font.SysFont('segoescript', 22)
textSurfaceObj8 = fontObj8.render('Second Life', True, ORANGE)

fontObj6 = pygame.font.SysFont('segoescript', 22)
textSurfaceObj6 = fontObj6.render('Set', True, ORANGE)

fontObj9 = pygame.font.SysFont('segoescript', 22)
textSurfaceObj9 = fontObj9.render('SCORE: ', True, ORANGE)

fontObj11 = pygame.font.SysFont('segoescript', 22)
textSurfaceOb11 = fontObj11.render('CPU Won', True, ORANGE)

fontObj12 = pygame.font.SysFont('segoescript', 22)
textSurfaceObj12 = fontObj12.render('You Won', True, ORANGE)

points="80"

fontObj7 = pygame.font.SysFont('segoescript', 22)
textSurfaceObj7 = fontObj7.render('Taken', True, ORANGE)

fontObj3 = pygame.font.SysFont('arialbold', 35)
textSurfaceObj3 = fontObj3.render('Pick a Card Please', True, RED)

fontObj4 = pygame.font.SysFont('arialbold', 35)
textSurfaceObj4 = fontObj4.render('Throw a Card Please', True, RED)

fontObj1 = pygame.font.SysFont('Arialbold', 40)
textSurfaceObj1 = fontObj1.render('CPU', True, BLACK)

fontObj2 = pygame.font.SysFont('Arialbold', 40)
textSurfaceObj2 = fontObj2.render(s, True, BLACK)

positions=[(11+80*i,594) for i in range(14)]
positionsref=positions.copy()
lenm=14
m=[False for i in range(lenm)]
listofcards=[]
listofimages=[]
for i in listofcards:
    cardImg=pygame.image.load(r"cards\\"+str(i)+".png")
    listofimages.append(cardImg)
discardclick=False
stockclick=False
discardcord=(600,270)
cardclick=False

def checkfirstlifeplayer(l):
    lenl=len(l)
    x=[]
    firstlife=False
    for i in range(lenl):
        c=1
        currcard=l[i]
        for j in range(i+1,lenl):
            if currcard[0]==l[j][0] and di[currcard[1:]]+c==di[l[j][1:]]:
                c+=1
            else:
                x.append(c)
                break
            if j==lenl-1:
                x.append(c)
    x.append(1)
    if max(x)>=3:
        return True,max(x),x.index(max(x)),x
    return False,0,0

def checksecondlifeplayer(l,click,firstind):
    p=l.copy()
    jokerused=False
    c=1
    if click<firstind:
        for i in range(click,firstind):
            if di[p[i][1:]]+1==di[p[i+1][1:]]:
                c+=1
            elif p[i+1] in jokers and not jokerused:
                c+=1
                jokerused=True
                p[i+1]=p[i][0]+dix[di[p[i][1:]]+1]
            elif p[click] in jokers:
                c=2
                for i in range(click+1,firstind):
                    if di[p[i][1:]]+1==di[p[i+1][1:]]:
                        c+=1
            else:
                break
    else:
        for i in range(click,len(l)-1):
            if p[i][0]==p[i+1][0] and di[p[i][1:]]+1==di[p[i+1][1:]]:
                c+=1
            elif p[i+1] in jokers and not jokerused:
                c+=1
                jokerused=True
                p[i+1]=p[i][0]+dix[di[p[i][1:]]+1]
            elif p[click] in jokers and not jokerused:
                c=2
                for i in range(click+1,len(p)-1):
                    if p[i][0]==p[i+1][0] and di[p[i][1:]]+1==di[p[i+1][1:]]:
                        c+=1
                break
            else:
                break
    return c

def setchecker(l):
    lenl=len(l)
    x=[]
    for i in range(lenl-2):
        c=1
        jokerused=False
        if l[i]=="Joker":
            c=2
            for j in range(i+1,min(i+3,lenl-1)):
                if l[j][0]!=l[j+1][0] and di[l[j][1:]]==di[l[j+1][1:]]:
                    c+=1
                else:
                    break
            x.append(c)
        else:
            suit=l[i][0]
            setpossibilities=[]
            for j in range(4):
                if suit!=suits[j]:
                    setpossibilities.append(suits[j]+l[i][1:])
            for j in range(i+1,min(i+4,lenl)):
                if l[j] in setpossibilities:
                    c+=1
                    setpossibilities.remove(l[j])
                elif l[j] in jokers and not jokerused:
                    c+=1
                    jokerused=True
                elif l[i] in jokers and j==i+1:
                    c=2
                    if l[i+1]=="Joker":
                        c=1
                    suit=l[i+1][0]
                    setpossibilities=[]
                    for q in range(4):
                        if suit!=suits[q]:
                            setpossibilities.append(suits[q]+l[i+1][1:])
                    for q in range(i+2,min(i+4,lenl)):
                        if l[q] in setpossibilities:
                            c+=1
                            setpossibilities.remove(l[q])
                    x.append(c)
                    break
                else:
                    x.append(c)
                    break
                if j==i+3 or j==lenl-1:
                    x.append(c)
                    break
    if x==[]:
        maxx=0
        maxindex=0
    else:
        maxx=max(x)
        maxindex=x.index(maxx)
    setformed=True
    if maxx<3:
        setformed=False
    return setformed,maxx,maxindex,x

def score(l):
    score=0
    if "xx" not in l:
        score=80
    else:
        for i in range(len(l)):
            if l[i] not in jokers:
                score+=dixy[l[i][1:]]
    return score
cpulist=cpu.copy()
cpu=sortcards(cpu)
listofcards=player1
stockpile=deck
while True:
    listofused=listofcards.copy()
    movemade=0
    cardclickcounter=0
    '''backg=pygame.image.load(r"backg5.jpg").convert()
    backg=pygame.transform.scale(backg,(1130,700))
    DISPLAYSURF.blit(backg,(0,0))'''
    DISPLAYSURF.fill(BLACK)
    cardImg2=pygame.image.load(r"cards\\"+t+".png")
    if len(discardpile)>0:
        cardImg3=pygame.image.load(r"cards\\"+discardpile[-1]+".png")
        DISPLAYSURF.blit(cardImg3,(600,270))
    else:
        pygame.draw.rect(DISPLAYSURF, BRIGHTBLUE, (600,270,71,96),2)
    x,y=pygame.mouse.get_pos()
    DISPLAYSURF.blit(textSurfaceObj,(582,240))
    DISPLAYSURF.blit(textSurfaceObj1,(15,120))
    DISPLAYSURF.blit(textSurfaceObj2,(15, 555))
    DISPLAYSURF.blit(cardImg2,(250,270))
    DISPLAYSURF.blit(cardImg1,(350,270))
    DISPLAYSURF.blit(jokericon,(295,244))
    if len(listofcards)==13:
        DISPLAYSURF.blit(textSurfaceObj3,(435, 520))
    else:
        DISPLAYSURF.blit(textSurfaceObj4,(435, 520))
    firstlifecheck=checkfirstlifeplayer(listofcards)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cardImg3.get_rect(topleft=(600,270)).collidepoint(event.pos) and len(listofcards)==13:
                discardclick=True
            else:
                discardclick=False
            if cardImg1.get_rect(topleft=(350,270)).collidepoint(event.pos) and len(listofcards)==13:
                stockclick=True
            else:
                stockclick=False
            for i in range(len(listofimages)):
                if listofimages[i].get_rect(topleft=positions[i]).collidepoint(event.pos):
                    m[i]=True
                    clickedcard=i
                    cardclickcounter+=1
            if cardclickcounter==0:
                cardclick=False
            else:
                cardclick=True
        elif event.type == pygame.MOUSEBUTTONUP:
            newpos=int((x-46.5)//80)
            if 546<y<642 and cardclick:
                currim=listofcards[clickedcard]
                if newpos>clickedcard:
                    for i in range(clickedcard,newpos):
                        listofcards[i]=listofcards[i+1]
                    listofcards[newpos]=currim
                elif newpos==clickedcard:
                    listofcards[newpos]=listofcards[clickedcard]
                    secondlife=checksecondlifeplayer(listofcards,clickedcard,firstlifecheck[2])
                    secondlifes=(secondlife,clickedcard)
                else:
                    for i in range(clickedcard,newpos,-1):
                        listofcards[i]=listofcards[i-1]
                    listofcards[newpos+1]=currim
            if discardclick and len(listofcards)==13:
                listofcards.append(discardpile.pop())
            elif stockclick and len(listofcards)==13:
                if 350<x<421 and 270<y<366:
                    listofcards.append(stockpile.pop(-1))
            elif 564.5<x<706.5 and 222<y<414 and len(listofcards)==14 and cardclick:
                discardpile.append(listofcards.pop(clickedcard))
                movemade=1
            positions=positionsref.copy()
            m=[False for i in range(lenm)]
        elif event.type==QUIT:
            pygame.quit()
            sys.exit()
    for i in range(lenm):
        if m[i]:
            positions[i]=(x-35.5,y-48)
    listofimages=[]
    for i in listofcards:
        cardImg=pygame.image.load(r"cards\\"+str(i)+".png")
        listofimages.append(cardImg)
    set2diff=False
    set2diff1=False
    if not firstlifecheck[0]:
        set1=setchecker(listofcards)
    else:
        set1=setchecker(listofcards[:firstlifecheck[2]])
    if not firstlifecheck[0] and set1[0]:
        set2=setchecker(listofcards[:set1[2]]+listofcards[set1[1]+set1[2]:])
        set2diff=True
    elif firstlifecheck[0]:
        set2=setchecker(listofcards[firstlifecheck[2]+firstlifecheck[1]:])
        set2diff1=True
    else:
        set2=setchecker(listofcards)
    for i in range(lenm):
        if len(listofcards)!=13 or i!=13:
            DISPLAYSURF.blit(listofimages[i],positions[i])
            pygame.draw.rect(DISPLAYSURF, BRIGHTBLUE, (11+80*i,594,71,96),2)
    if firstlifecheck[0]:
        for j in range(firstlifecheck[2],firstlifecheck[2]+firstlifecheck[1]):
            listofused[j]="xx"
        rectanglesurf=pygame.Surface((80*(firstlifecheck[1]-1)+71,40))
        DISPLAYSURF.blit(rectanglesurf,(11+80*firstlifecheck[2],660))
        DISPLAYSURF.blit(textSurfaceObj5,(80*firstlifecheck[2]+(80*(firstlifecheck[1]-1))//2-5,661))
        if firstlifecheck[1]==3 and secondlifes[0]>=4 or firstlifecheck[1]>=4 and secondlifes[0]>=3:
            for j in range(secondlifes[1],secondlifes[0]+secondlifes[1]):
                listofused[j]="xx"
            rectanglesurf=pygame.Surface((80*(secondlifes[0]-1)+71,40))
            DISPLAYSURF.blit(rectanglesurf,(11+80*secondlifes[1],660))
            DISPLAYSURF.blit(textSurfaceObj8,(80*secondlifes[1]+(80*(secondlifes[0]-1))//2-5,661))
    if set1[0]:
        for j in range(set1[2],set1[2]+set1[1]):
            listofused[j]="xx"
        rectanglesurf=pygame.Surface((80*(set1[1]-1)+71,40))
        DISPLAYSURF.blit(rectanglesurf,(11+80*set1[2],660))
        DISPLAYSURF.blit(textSurfaceObj6,(80*set1[2]+(80*(set1[1]-1))//2+15,661))
    if set2[0]:
        for j in range(set2[2],set2[2]+set2[1]):
            listofused[j]="xx"
        if set2diff:
            if set2[2]>=set1[2]:
                set2=(set2[0],set2[1],set2[2]+set1[1],set2[3])
        if set2diff1:
            set2=(set2[0],set2[1],set2[2]+firstlifecheck[1]+firstlifecheck[2],set2[3])
        rectanglesurf=pygame.Surface((80*(set2[1]-1)+71,40))
        DISPLAYSURF.blit(rectanglesurf,(11+80*set2[2],660))
        DISPLAYSURF.blit(textSurfaceObj6,(80*set2[2]+(80*(set2[1]-1))//2+15,661))
    for i in range(13):
        DISPLAYSURF.blit(cardImg1,(11+80*i,10))
    if movemade==1:
        cardImg3=pygame.image.load(r"cards\\"+discardpile[-1]+".png")
        DISPLAYSURF.blit(cardImg3,(600,270))
        pygame.display.update()
        pygame.time.delay(800)
        discardtaken=TakeCard(cpu,discardpile[-1],deck[-1])
        cardImg3=pygame.image.load(r"cards\\"+discardpile[-1]+".png")
        DISPLAYSURF.blit(cardImg3,(600,270))
        DISPLAYSURF.blit(cardImg1,(11+80*13,10))
        if discardtaken:
            DISPLAYSURF.blit(textSurfaceObj7,(610,210))
        else:
            DISPLAYSURF.blit(textSurfaceObj7,(350,230))
        pygame.display.update()
        pygame.time.delay(1000)
        ThrowCard(cpu)
        cardImg3=pygame.image.load(r"cards\\"+discardpile[-1]+".png")
        DISPLAYSURF.blit(cardImg3,(600,270))
        pygame.draw.rect(DISPLAYSURF, BLACK, (11+80*13,10,71,96))
        pygame.display.update()
        pygame.time.delay(300)
    points=str(score(listofused))
    fontObj10 = pygame.font.SysFont('segoescript', 22)
    textSurfaceObj10 = fontObj10.render(points, True, ORANGE)
    DISPLAYSURF.blit(textSurfaceObj9,(900,350))
    DISPLAYSURF.blit(textSurfaceObj10,(1000,350))
    if checksecondlife(cpu):
        listofimages1=[]
        for i in cpulist:
            cardImg=pygame.image.load(r"cards\\"+str(i)+".png")
            listofimages1.append(cardImg)
        DISPLAYSURF.fill(BLACK)
        for i in range(13):
            DISPLAYSURF.blit(listofimages1[i],positions[i])
            pygame.draw.rect(DISPLAYSURF, BRIGHTBLUE, (11+80*i,10,71,96),2)
        DISPLAYSURF.blit(textSurfaceObj11,(550,350))
        pygame.time.delay(10000)
        pygame.quit()
        sys.exit()
    if points=="0":
        DISPLAYSURF.fill(BLACK)
        for i in range(13):
            DISPLAYSURF.blit(listofimages[i],positions[i])
            pygame.draw.rect(DISPLAYSURF, BRIGHTBLUE, (11+80*i,300,71,96),2)
        DISPLAYSURF.blit(textSurfaceObj12,(550,350))
        pygame.time.delay(10000)
        pygame.quit()
        sys.exit()
    pygame.display.update()

