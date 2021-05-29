import pygame, sys
from objects import * #objects.py

pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = (1200, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((600, 400))

animation_database = {}

def readanim(filename): #reads animation data from filename and stores it in animation_database. there's probably a better way to do this but idk
    global animation_database
    animfile = open(filename)
    animname=""
    framelist=[]
    durationlist=[]
    framesleft=0
    loop=False
    sound=None
    for line in animfile.readlines(): #each line = one frame
        if line[0]=='#': continue #skip comment lines
        if framesleft==0: #read animation line
            if animname!="": #if there was a previous animation, store it in the database
                animation_database[animname] = [framelist,durationlist,loop,sound]
            framelist=[]
            durationlist=[]
            data = line.split()
            animname = data[0]
            framesleft = int(data[1])
            loop = data[2]
            if loop=="True":
                loop=True
            else:
                loop=False
            sound = data[3]
            if sound=="None": sound=None
        else: #read frame line
            data = line.split()
            image=pygame.image.load(animname+"\\"+animname+"_"+str(len(durationlist))+".png").convert()
            image.set_colorkey((255,255,255))
            durationlist.append(int(data[0]))
            
            movement=data[1].split(",")
            movement[0]=float(movement[0])
            movement[1]=float(movement[1])
            
            imageofs=data[2].split(",")
            imageofs[0]=int(imageofs[0])
            imageofs[1]=int(imageofs[1])
            
            rect=data[3].split(",")
            rect[0]=int(imageofs[0])
            rect[1]=int(rect[1])
            rect[2]=int(rect[2])
            rect[3]=int(rect[3])
            
            hurtboxnum=int(data[4])
            hurtboxes=[]
            for i in range(5,5+hurtboxnum):
                hurtbox=data[i].split(",")
                hurtboxes.append([int(hurtbox[0]),int(hurtbox[1]),int(hurtbox[2]),int(hurtbox[3])])
            
            hitboxnum=int(data[5+hurtboxnum])
            hitboxes=[]
            for i in range(6+hurtboxnum,6+hurtboxnum+hitboxnum):
                hitbox=data[i].split(",")
                hitboxes.append([int(hitbox[0]),int(hitbox[1]),int(hitbox[2]),int(hitbox[3])])
            
            damage = int(data[6+hurtboxnum])
            
            framelist.append(Frame(movement,image,imageofs,rect,hurtboxes,hitboxes,damage))
            framesleft-=1
    #store last read animation
    animation_database[animname] = [framelist,durationlist,loop,sound]

def gameloop():
    global animation_database
    player = Character([0,0])
    player.setanimation(animation_database["walk"])
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        player.update()
        
        display.fill([100,200,255])
        display.blit(player.image,[int(player.pos[0]+player.imageofs[0]),int(player.pos[1]+player.imageofs[1])])
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)

readanim("animdata.txt")
print(animation_database)
gameloop()
