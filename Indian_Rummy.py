import pygame
from random import *
import bisect
import math
deck=[]
discardpile=["h4","d9"]
player1=[]
cpu=[]
jokers=[]
values=["1","2","3","4","5","6","7","8","9","90","J","Q","k"]
suits=["c","d","h","s"]
d={"c":0,"d":1,"h":2,"s":3}
di={"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"90":10,"Q":12,"J":11,"k":13,"oker":0,"x":-1}
dix={1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"90",11:"J",13:"k",12:"Q",0:"oker",-1:"x"}
dixy={"1":10,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"90":10,"Q":10,"J":10,"k":10,"oker":0,"x":0}


def makeDeck():
    global deck, values, suits
    for i in suits:
        for j in values:
            deck.append(i+j)
    deck+=["Joker","Joker"]
    deck*=2

def randomshuffle():
    global deck
    shuffle(deck)

def dealcards():
    global deck, player1,cpu
    player1=deck[:13]
    cpu=deck[13:26]
    deck=deck[26:]
    discardpile.append(deck.pop(0))

def makeJoker():
    global jokers
    x=randint(0,len(deck)-1)
    extrajoker=deck.pop(x)
    extrajokervalue=extrajoker[1:]
    if extrajoker!="Joker":
        jokers=[(i+extrajokervalue) for i in suits]*2
        jokers+=["Joker" for i in range(4)]
        jokers.remove(extrajoker)
    else:
        jokers=["Joker" for i in range(3)]
    return extrajoker

def sortcards(l):
    global jokers
    l.sort()
    jo=[]
    cl=[]
    di=[]
    he=[]
    sp=[]
    for i in range(len(l)):
        if l[i] in jokers:
            jo.append(l[i])
        else:
            if l[i][0]=="c":
                cl.append(l[i])
            if l[i][0]=="d":
                di.append(l[i])
            if l[i][0]=="h":
                he.append(l[i])
            if l[i][0]=="s":
                sp.append(l[i])
    ma=[cl,di,he,sp,jo]
    return ma

def checkPairs(l):
    y=[]
    for i in range(4):
        lis=l[i]
        c=1
        q=[0]
        for j in range(len(lis)-1):
            t=lis[j][1:]
            v=lis[j+1][1:]
            if di[t]==di[v]-1:
                c+=1
            else:
                q.append(c)
                c=1
        q.append(c)
        y.append(max(q))
    return max(y),y

def TakeCard(l,fu,fd):
    global jokers,d
    if fu in jokers:
        l[-1].append(fu)
        del discardpile[-1]
        discardtaken=True
    else:
        fusuit=fu[0]
        fupos=d[fusuit]
        x=l[fupos]
        ind=bisect.bisect(x,fu)
        t=fu[1:]
        if ind!=len(x) and ind!=0 and fu not in x:
            v=x[ind][1:]
            y=x[ind-1][1:]
            if di[t]-di[y]==1 or di[v]-di[t]==1:
                l[fupos].insert(ind,discardpile.pop(-1))
                discardtaken=True
            else:
                fdsuit=fd[0]
                fdpos=d[fdsuit]
                bisect.insort(l[fdpos],fd)
                del deck[-1]
                discardtaken=False
        else:
            if fd in jokers:
                l[-1].append(fd)
                del deck[-1]
                discardtaken=False
            else:
                fdsuit=fd[0]
                fdpos=d[fdsuit]
                bisect.insort(l[fdpos],fd)
                del deck[-1]
                discardtaken=False
    return discardtaken

def ThrowCard(l):
    for i in range(4):
        c=[]
        x=l[i]
        if x==[]:
            continue
        for j in range(len(x)-1):
            c.append(di[x[j+1][1:]]-di[x[j][1:]])
        if c==[]:
            discardpile.append(l[i].pop(0))
            break
        elif c.count(0)!=0:
            indo=c.index(0)
            discardpile.append(l[i].pop(indo))
            break
        else:
            maxc=max(c)
            if maxc>2:
                c=[math.inf]+c+[math.inf]
                indmax=c.index(maxc)
                if c[indmax-1]>c[indmax+1]:
                    discardpile.append(l[i].pop(indmax-1))
                else:
                    discardpile.append(l[i].pop(indmax))
                break
            if i==3 and maxc<2 and len(l[i])>=1:
                discardpile.append(l[i].pop())
            elif i==3 and maxc<2 and len(l[i])<1:
                discardpile.append(l[0].pop())

def checkfirstlife(l):
    m,n=checkPairs(l)
    if m>=3:
        return True,m,n
    return False,m,n

def checksecondlife(l):
    x,y,z=checkfirstlife(l)
    t=[]
    if x:
        q=sorted(z)
        r= q[-2]
        if y>=7 or (y>=4 and r>=3) or (y==3 and r>=4):
            return True
        elif ((y==6) or (y>=4 and r==2) or (y==3 and r==3)) and len(l[-1])!=0:
            return True
        elif y==4 and r==1 and len(l[-1])!=0:
            u=z.index(4)
            for i in range (4):
                if i !=u:
                    for j in range (len(l[i])-1):
                        if di[l[i][j+1][1:]]-di[l[i][j][1:]]==2:
                            return True
                            break
        elif y==3 and r==2 and len(l[-1])!=0:
            for i in range(len(z)):
                if z[i]==2:
                    t.append(i)
            for i in range(len(t)):
                w=l[t[i]]
                k=list(map(lambda x: di[x[1:]], w))
                for i in range(len(k)-2):
                    a=[k[i+1]-k[i],k[i+2]-k[i+1]]
                    a.sort()
                    if a==[1,2]:
                        return True
        return False
    return False

makeDeck()
randomshuffle()
dealcards()
t=makeJoker()




