from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt

#making the window
root = Tk()
root.title('Bubble Blaster')
c = Canvas(root, width=800, height = 500, bg='darkblue')
c.pack()

#bonus addition
timeLimit = 30
bonusScore = 1000
bonus = 0
end = time() + timeLimit

#making variables
bubble_id = []
bubble_r = []
bubble_spd = []
gap = 100
score = 0

#making the ship
ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship_id2 = c.create_oval(0, 0, 30, 30, outline = 'red')
SHIP_R = 15
c.move(ship_id, 400, 250)
c.move(ship_id2, 400, 250)

#control buttons
def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -10)
        c.move(ship_id2, 0, -10)
    elif event.keysym == 'Down':
        c.move(ship_id, 0, 10)
        c.move(ship_id2, 0, 10)
    elif event.keysym == 'Left':
        c.move(ship_id, -10, 0)
        c.move(ship_id2, -10, 0)
    elif event.keysym == 'Right':
        c.move(ship_id, 10, 0)
        c.move(ship_id2, 10, 0)
c.bind_all('<Key>', move_ship)

#creating bubbles function
def create_bubble():
    x = 800+gap
    y = randint(0, 500)
    r = randint(10, 30)
    id1 = c.create_oval(x-r, y-r, x+r, y+r, outline = 'white')
    bubble_id.append(id1)
    bubble_r.append(r)
    bubble_spd.append(randint(1, 10))

def movebubs():
    for i in range(len(bubble_id)):
        c.move(bubble_id[i], -bubble_spd[i], 0)

def getcords(idnum):
    pos = c.coords(idnum)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y

#deleting bubble
def delbub(i):
    del bubble_r[i]
    del bubble_spd[i]
    c.delete(bubble_id[i])
    del bubble_id[i]

def cleanup():
    for i in range(len(bubble_id)-1, -1, -1):
        x, y = getcords(bubble_id[i])
        if x < -gap:
            delbub(i)

#counting score
def dist(id1, id2):
    x1, y1 = getcords(id1)
    x2, y2 = getcords(id2)
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def collision():
    points = 0
    for bub in range(len(bubble_id)-1, -1, -1):
        if dist(ship_id2, bubble_id[bub]) < (15 + bubble_r[bub]):
            points += (bubble_r[bub] + bubble_spd[bub])
            delbub(bub)
    return points

#score table
c.create_text(50, 30, text = 'TIME', fill='white')
c.create_text(150, 30, text = 'SCORE', fill = 'white')
timetext = c.create_text(50, 50, fill='white')
scoretext = c.create_text(150, 50, fill='white')
def showscore(score):
    c.itemconfig(scoretext, text=str(score))
def showtime(timeleft):
    c.itemconfig(timetext, text=str(timeleft))

#MAIN
while time() < end:
    if randint(1, 10) == 1:
        create_bubble()
    movebubs()
    cleanup()
    score += collision()
    if (int(score / bonusScore)) > bonus:
        bonus += 1
    showscore(score)
    showtime(int(end-time()))
    root.update()
    sleep(0.01)

c.create_text(400, 250, text='GAME OVER', fill='white', font = ('Helvetica', 30))
c.create_text(400, 280, text=f'Score: {score}', fill='white',)
c.create_text(400, 295, text=f'Bonus time: {bonus*timeLimit}', fill='white')

root.mainloop()
