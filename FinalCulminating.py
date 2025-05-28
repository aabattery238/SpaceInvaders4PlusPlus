from pygame import *
from pygame.locals import *
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

#starts here
pygame.init()
screen = pygame.display.set_mode((800,800))
color = [(255,0,0),(0,255,0)]
pygame.display.set_caption('im pygaming it')
clock = pygame.time.Clock()
running = True
x = 300
y = 300
speed = 10
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[K_d]:
        x+=speed
    if keys[K_a]:
        x-=speed
    if keys[K_w]:
        y-=speed
    if keys[K_s]:
        y+=speed
    clock.tick(60)
    screen.fill((0, 0, 0)) 
    fish = pygame.draw.circle(screen,(255,0,255),(x,y),(10),5)
    pygame.display.update()
pygame.quit()   
