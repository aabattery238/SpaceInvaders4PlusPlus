from pygame import *

class bullet:
    def __init__(movementSpeed, angle):
        self.movementSpeed = movementSpeed
        self.angle = angle

shoot = bullet(6, 60)
print(shoot.move)
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
