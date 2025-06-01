import pygame
from pygame import *
from pygame.locals import *
import random
from math import *


bulletRadius = 5
enemyRadius = 10

class bullet:
    def __init__(self, position, direction, speed, existance, colour):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.existance = existance
        self.colour = colour
        self.visual = pygame.draw.circle(mainscreen, self.colour, self.position, 5)

    def update(self):
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
        self.visual = pygame.draw.circle(mainscreen, self.colour, self.position, 5)
    
    def draw(self, screen):
        self.visual = pygame.draw.circle(screen, self.colour, self.position, 5)

class enemy:
    def __init__(self, position, existance):
        self.position = position
        self.existance = existance

    def draw(self, surface):
        self.visual = pygame.draw.circle(surface, (255, 0, 0), self.position, enemyRadius)

def isStartClicked(mousePos):
    global mainMenuState
    pygame.event.get()
    if mousePos[0] in range(startButtonRect.x,startButtonRect.x+320) and mousePos[1] in range(startButtonRect.y,startButtonRect.y+130) and event.type == pygame.MOUSEBUTTONUP:
        mainMenuState = False
    startButtonRect.clamp_ip(mainscreen.get_rect())
    mainscreen.blit(scaledStartButtonAsset, startButtonRect)


pygame.init()
characterAsset = pygame.image.load("playersprite1.png")
characterRect = characterAsset.get_rect(center=(300, 300))
startButtonAsset = pygame.image.load("startbutton.png")
scaledStartButtonAsset = pygame.transform.scale(startButtonAsset, (startButtonAsset.get_width() * 10, startButtonAsset.get_height() * 10))
startButtonRect = scaledStartButtonAsset.get_rect(center=(400,400))

bulletCooldownLength = 1
bulletCooldown = 0
playerSpeed = 5
defaultBulletSpeed = 10
clock = pygame.time.Clock()
mainscreen = pygame.display.set_mode((800,800))
existingBullets = [bullet(characterRect.midtop, [0, 0], defaultBulletSpeed, False, (255, 255, 255))]
existingEnemies = [enemy((400, 400), True)]
angle = 0
running = True
mainMenuState = True

while running:
    clock.tick(60)
    mainscreen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()
    
    
    if mainMenuState == True:
        isStartClicked(mousePos)

    elif mainMenuState == False:
        if keys[K_d]:
            characterRect.x += playerSpeed
        if keys[K_a]:
            characterRect.x -= playerSpeed
        if keys[K_w]:
            characterRect.y -= playerSpeed
        if keys[K_s]:
            characterRect.y += playerSpeed

        if keys[K_SPACE] and bulletCooldown <= 0:
            print("cooldown")
            mouseX, mouseY = pygame.mouse.get_pos()
            dx, dy = mouseX - characterRect.x, mouseY - characterRect.y
            distance = hypot(dx, dy)
            
            if distance != 0:
                print("distance")
                direction = [dx / distance, dy / distance]
                existingBullets.append(bullet([characterRect.x, characterRect.y], direction, defaultBulletSpeed, True, (255, 255, 255)))
                bulletCooldown = bulletCooldownLength

        for bullets in existingBullets:
            if bullets.existance:
                bullets.update()
                bullets.draw(mainscreen)

        for enemies in existingEnemies:
            enemy.draw(enemies, mainscreen)
            
            for bullets in existingBullets:
                if (enemies.visual).colliderect(bullets.visual) and enemies.existance and bullets.existance:
                    bullets.existance = False
                    enemies.existance = False
                    existingBullets.remove(bullets)
                    existingEnemies.remove(enemies)
                    newPos = (random.randint(0, 800), random.randint(0, 800))
                    existingEnemies.append(enemy(newPos, True))
                    break

        bulletCooldown -= 0.1
        mouseX, mouseY = pygame.mouse.get_pos()

        angle = degrees(atan2(mouseY - characterRect.centery, mouseX - characterRect.centerx)) + 90

        scaledAsset = pygame.transform.scale(characterAsset, (characterAsset.get_width() * 3, characterAsset.get_height() * 3))
        rotatedAsset = pygame.transform.rotate(scaledAsset, -angle) 

        newRect = rotatedAsset.get_rect(center=characterRect.center)

        mainscreen.blit(rotatedAsset, newRect)

    pygame.display.flip()

pygame.quit()
