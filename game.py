from tkinter import *
from random import randint
from time import sleep
from math import sqrt

#parameters and variables
WIDTH = 1366
HEIGHT = 768
BUB_CHANCE = 10
TIME_LIMIT = 60
SHIP_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
SHIP_SPEED = 15
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPEED = 10
GAP = 100

score = 0
playtime = 0
bub_id = list()
bub_r = list()
bub_speed = list()

root = Tk()
root.title('Buuble Blaster')
c = Canvas(root, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()

ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship_id2 = c.create_oval(0, 0, 30, 30, outline='red')

c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)

def moveShip(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SHIP_SPEED)
        c.move(ship_id2, 0, -SHIP_SPEED)
    elif event.keysym == 'Down':
        c.move(ship_id, 0, SHIP_SPEED)
        c.move(ship_id2, 0, SHIP_SPEED)
    elif event.keysym == 'Left':
        c.move(ship_id, -SHIP_SPEED, 0)
        c.move(ship_id2, -SHIP_SPEED, 0)
    elif event.keysym == 'Right':
        c.move(ship_id, SHIP_SPEED, 0)
        c.move(ship_id2, SHIP_SPEED, 0)
c.bind_all('<Key>', moveShip)

def createBubble():
    x = WIDTH+GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    id1 = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPEED))

def moveBubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)

def getCoords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y

def deleteBubble(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]
    
def cleanUp():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = getCoords(bub_id[i])
        if x < -GAP:
            deleteBubble(i)

def distance(id1, id2):
    x1, y1 = getCoords(id1)
    x2, y2 = getCoords(id2)
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def collision():
    points = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub])<(SHIP_R+bub_r[bub]):
            points += (bub_r[bub]+bub_speed[bub])
            deleteBubble(bub)
    return points

#score and time table
c.create_text(50, 30, text='TIME', fill='white')
c.create_text(150, 30, text='SCORE', fill='white')
time_text = c.create_text(50, 50, fill='white')
score_text = c.create_text(150, 50, fill='white')
def show_score(score):
    c.itemconfig(score_text, text=str(score))
def show_time(time_left):
    c.itemconfig(time_text, text=str(time_left))

#MAIN GAME LOOP
while playtime<TIME_LIMIT:
    if randint(1, BUB_CHANCE) == 1:
        createBubble()
    moveBubbles()
    cleanUp()
    score += collision()
    show_score(score)
    show_time(int(playtime))
    root.update()
    sleep(0.01)
    playtime += 0.01

c.create_text(MID_X, MID_Y, text='GAME OVER', fill='white', font=('Impact', 30))
c.create_text(MID_X, MID_Y+30, text=f'Score: {str(score)}', fill='white')
