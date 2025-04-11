import random
import pygame
import tkinter as tk
from tkinter import messagebox
pygame.mixer.init()
eat_sound=pygame.mixer.Sound("sound/eating_sound.wav")
game_over_sound=pygame.mixer.Sound("sound/game_over.wav")

class cube(object):
    rows=20
    w=500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        if isinstance(start, tuple) and len(start) == 2:
            self.pos = start
        else:
            raise ValueError("start must be a tuple with two values (x, y)")
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self,dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self,surface, eyes=False):
        dis=self.w//self.rows
        i=self.pos[0]
        j=self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-1, dis-2))
        if eyes:
            centre=dis//2
            radius=3
            circleMiddle=(i*dis+centre-radius, j*dis+8)
            circleMiddle2=(i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class Snake(object):
    body=[]
    turns={}
    def __init__(self, color, pos,rows):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx=0
        self.dirny=1
        self.rows=rows

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.dirnx==0:
                self.dirnx=-1
                self.dirny=0
                self.turns[self.head.pos]=[self.dirnx,self.dirny]
        elif keys[pygame.K_RIGHT]:
            if self.dirnx==0:
                self.dirnx=1
                self.dirny=0
                self.turns[self.head.pos] = [self.dirnx,self.dirny]
        elif keys[pygame.K_UP]:
            if self.dirny==0:
                self.dirny=-1
                self.dirnx=0
                self.turns[self.head.pos] = [self.dirnx,self.dirny]
        elif keys[pygame.K_DOWN]:
            if self.dirny==0:
                self.dirny=1
                self.dirnx=0
                self.turns[self.head.pos] = [self.dirnx, self.dirny]

        for i in range(len(self.body)-1,0,-1):
            self.body[i].pos = self.body[i-1].pos

        head=self.body[0]
        head.move(self.dirnx, self.dirny)

        # for x in range(1,len(self.body)):
        #     if self.body[x].pos==head.pos:
        #         print("Scores: ", len(self.body))
        #         message_box("You Lost!","Play again...")
        #         self.reset(10,10)
        #         break
        # if head.pos in self.turns:
        #     turn=self.turns.pop(head.pos)
        #     head.move(turn[0],turn[1])

        if head.pos[0]<0 or head.pos[0]>=self.rows or head.pos[1]<0 or head.pos[1]>self.rows:
            print("Game Over! The snake hit the border!")
            game_over_sound.play()
            message_box("Game Over","You hit the border. Play again?")
            self.reset((10,10))

        for x in range(1, len(self.body)):
            if self.body[x].pos == self.head.pos:
                print("Game Over! The snake hit itself!")
                game_over_sound.play()
                message_box("Game Over","Play again...")
                self.reset((10,10))

    def reset(self, pos):
        self.head = cube (pos)
        self.body=[]
        self.body.append(self.head)
        # self.turns={}
        self.dirnx=0
        self.dirny=1

    def addCube(self):
        tail=self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx==1 and dy==0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx==-1 and dy==0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx==0 and dy==1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx==0 and dy==-1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx=dx
        self.body[-1].dirny=dy

    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i==0:
                c.draw(surface,True)
            else:
                c.draw(surface)

def drawGrid(w,rows,surface):
    sizeBtwn=w/rows
    x=0
    y=0
    for row in range(rows):
        x=x+sizeBtwn
        y=y+sizeBtwn

        pygame.draw.line(surface, (255,255,255),(x,0),(x,w))
        pygame.draw.line(surface, (255, 255, 255), (0,y), (w,y))
def redrawWindow(surface,score):
    global width, rows, s, snack1, snack2
    surface.fill((0,0,0))
    drawGrid(width, rows, surface)
    s.draw(surface)
    snack1.draw(surface)
    snack2.draw(surface)

    font= pygame.font.SysFont('arial',30)
    score_text=font.render(f"Score:{score}", True, (255,255,255))
    surface.blit(score_text,(10,10))

    pygame.display.update()

def randomSnack(rows, item, snack1=None, snack2=None):
    positions=item.body

    while True:
        x=random.randrange(rows)
        y=random.randrange(rows)
        if len(list(filter(lambda z:z.pos ==(x,y),positions)))>0:
            continue
        if snack1 and snack1.pos==(x,y):
            continue
        if snack2 and snack2.pos==(x,y):
            continue

        break
    return (x,y)

def message_box(subject, content):
    root=tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack1, snack2
    width = 500
    height = 500
    rows = 20
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    s = Snake((255, 0, 0), (10, 10),rows)

    snack1 = cube(randomSnack(rows, s), color=(0, 255, 0))
    snack2 = cube(randomSnack(rows, s), color=(0, 255, 0))

    score=0
    flag = True

    clock = pygame.time.Clock()


    while flag:
        pygame.time.delay(50)
        clock.tick(10)

        s.move()

        if s.body[0].pos == snack1.pos:
            s.addCube()
            snack1 = cube(randomSnack(rows, s), color=(0, 255, 0))
            score += 1
            eat_sound.play()
        elif s.body[0].pos == snack2.pos:
            s.addCube()
            snack2 = cube(randomSnack(rows, s), color=(0, 255, 0))
            score += 1
            eat_sound.play()

        redrawWindow(win, score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

    pygame.quit()

main()
