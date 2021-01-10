import pygame
import time
true=True

none='none'
wall='wall'
Nwall='Nwall'
cross='cross'
shpath='shpath'
objective='objective'
start='start'


pygame.init()

WIDTH=600
HEIGHT=600
scr=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PATHFINDER')

WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)
BLUE=(0,255,255)
GRAY=(200,200,200)
BLACK=(0,0,0)


class path():
    def __init__(self, x, y, mode, weight=1, producer=None):
        self.x=x
        self.y=y
        self.mode=mode
        self.weight=weight
        self.rX=range(self.x,self.x+19)
        self.rY=range(self.y,self.y+19)
        self.producer=producer

    def draw(self):
        if self.mode==none:
            pygame.draw.rect(scr, WHITE, (self.x, self.y, 20, 20))
        elif self.mode==cross:
            pygame.draw.rect(scr, GREEN, (self.x, self.y, 20, 20))
        elif self.mode==objective:
            pygame.draw.rect(scr, YELLOW, (self.x, self.y, 20, 20))
        elif self.mode==start:
            pygame.draw.rect(scr, RED, (self.x, self.y, 20, 20))
        elif self.mode==wall:
            pygame.draw.rect(scr, BLACK, (self.x, self.y, 20, 20))
        elif self.mode==Nwall:
            pygame.draw.rect(scr, BLACK, (self.x, self.y, 20, 20))
        elif self.mode==shpath:
            pygame.draw.rect(scr, BLUE, (self.x, self.y, 20, 20))

        if self.mode!=wall:
            if self.mode!=Nwall:
                for i in range(4):
                    pygame.draw.rect(scr, GRAY, (self.x-i,self.y-i,20,20), 1)




NOTGO=[31, 61, 91, 121, 151, 181, 211, 241, 271, 301, 331, 361, 391, 421, 451, 481, 511, 541, 571, 601, 631, 661, 691, 721, 751, 781, 811, 841, 871,
       30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720, 750, 780, 810, 840, 870, 900,
       0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
       872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899]

stpos=45
obpos=795
def prepare():
    global paths, passed, new_passed, x_pos, y_pos, T
    paths=[]
    passed=[]
    new_passed=[]


    x_pos=-20
    y_pos=0
    for i in range(901):
        x_pos+=20
        paths.append(path(x_pos, y_pos, none))
        if i%30==0 and i!=0:
            y_pos+=20
            x_pos=-20

    for n in NOTGO:
        paths[n].mode=Nwall

       

    paths[stpos].mode=start

    paths[obpos].mode=objective

    passed.append(paths[stpos])
    
    T=0

def semiR():
    global passed, new_passed, T
    passed=[]
    new_passed=[]
    paths[stpos].mode=start
    paths[obpos].mode=objective
    passed.append(paths[stpos])
    for pt in paths:
        if pt.mode==cross:
            pt.mode=none
        elif pt.mode==shpath:
            pt.mode=none

    T=0
        
    
prepare()

arround=[1,-1,30,-30]

T=0

def findpath():
    global passed, true, new_passed, Begin, T
    current=None
    for nod in passed:
        ind=paths.index(nod)
        for p in arround:
            if paths[ind+p].mode==none:
                paths[ind+p].mode=cross
                paths[ind+p].producer=paths[ind]
                new_passed.append(paths[ind+p])
                
                    
            elif paths[ind+p].mode==objective:
                Begin="Ready"
                paths[ind].mode=shpath
                current=paths[ind]
                for i in range(T-1):
                    current=current.producer
                    current.mode=shpath
                T=0
                break
                exit
                
                
    passed=new_passed[:]
    new_passed=[]
    T+=1


Begin="Ready"

mouse="draw"

ch="ST"

print("To build walls press the left button of your mouse\t To delete walls press 'e' and then press the left button of your mouse \n To delete all the walls and the path press 'r' \t To delete only the path but no the walls press 'a'")
print("To change the start square click on another square with the right button of your mouse\t To change the objective square press 'c' and then click on the left mouse button")

while true:
    scr.fill(BLACK)

    if Begin=="Go":
        findpath()

    
    for p in paths:
        p.draw()


    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            true=False
            break

        if event.type==pygame.MOUSEBUTTONDOWN and event.button==3:
            Mposition=pygame.mouse.get_pos()
            if ch=="ST":
                for p in paths:
                    if Mposition[0] in p.rX and Mposition[1] in p.rY:
                        if p.mode==none:
                            paths[stpos].mode=none
                            stpos=paths.index(p)
                            semiR()
                            Begin="Ready"
                            break
            else:
                for p in paths:
                    if Mposition[0] in p.rX and Mposition[1] in p.rY:
                        if p.mode==none:
                            paths[obpos].mode=none
                            obpos=paths.index(p)
                            semiR()
                            Begin="Ready"
                            break
                
                            

    if pygame.mouse.get_pressed()[0] and mouse=="draw":
        Mposition=pygame.mouse.get_pos()
        for p in paths:
            if Mposition[0] in p.rX and Mposition[1] in p.rY:
                if p.mode==none:
                    p.mode=wall

    elif pygame.mouse.get_pressed()[0] and mouse=="erase":
        Mposition=pygame.mouse.get_pos()
        for p in paths:
            if Mposition[0] in p.rX and Mposition[1] in p.rY:
                if p.mode==wall:
                    p.mode=none
        
    
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        Begin="Go"
        
        time.sleep(0.1)
        


    elif keys[pygame.K_r]:
        Begin="Ready"
        prepare()
        

    elif keys[pygame.K_a]:
        Begin="Ready"
        semiR()
        

    elif keys[pygame.K_e]:
        if mouse=="draw":
            mouse="erase"
        else:
            mouse="draw"

        time.sleep(0.1)

    elif keys[pygame.K_c]:
        if ch=="ST":
            ch="OB"
        else:
            ch="ST"

        time.sleep(0.1)
        

'''
MADE BY JAKI_2343
'''





