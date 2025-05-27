from pygame import *

up = "w"
down = "s"
right = ""
mainScreen =  display.set_mode((600, 800))
mainScreen.init()

running = True
while running:
    for event in event.get () :
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            draw.circle()
