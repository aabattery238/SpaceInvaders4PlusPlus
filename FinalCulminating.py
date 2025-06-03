import pygame
from pygame import *
from pygame.locals import *
import random
from math import *
import time
print('start')
levelDetails = {
    1 : {
        "waves" : 3,
        "enemies/wave" : 2
    }
}



clock = pygame.time.Clock()
mainscreen = pygame.display.set_mode((800,800))

class character:
    #Initialize Player Class
    def __init__(self, position):
        self.immunity = 0
        self.health = 5
        self.position = tuple(position)
        self.assets = [transform.scale_by(image.load("playersprite1.png"), 3), transform.scale_by(image.load("playersprite2.png"), 3)]
        self.rect = self.assets[0].get_rect(center = self.position)
        self.frameCounter = 0
        self.currentFrame = 0
        self.bulletCooldown = 0
        self.speed = 5

    def update(self):
        #Update the Frame of Class Character
        self.frameCounter += 1
        if self.frameCounter >= 10:
            self.currentFrame = (self.currentFrame + 1) % len(self.assets)
            self.frameCounter = 0

    def draw(self):
        #Draw the Image based on scaling, rotation and 
        mouseX, mouseY = pygame.mouse.get_pos()
        angle = degrees(atan2(mouseY - self.rect.centery, mouseX - self.rect.centerx)) + 90
        self.currentAsset = transform.rotate(self.assets[self.currentFrame], -angle)
        self.updatedRect = self.currentAsset.get_rect(center=self.rect.center)
        mainscreen.blit(self.currentAsset, self.updatedRect)

class bullet():
    #Initialize Bullet Class
    def __init__(self, shooter, position, direction, colour):
        self.shooter = shooter
        self.position = list(position)
        self.direction = list(direction)
        self.colour = tuple(colour)
        self.existance = True
        self.visual = draw.circle(mainscreen, self.colour, self.position, 5)

    def update(self):
        self.position[0] += self.direction[0] * 5
        self.position[1] += self.direction[1] * 5

    def draw(self):
        self.visual = pygame.draw.circle(mainscreen, self.colour, self.position, 5)
        


class enemy:
    #Initialize Enemy Class
    def __init__(self, position, direction, shootingSpeed, health, orbitRadius, enemyType):
        self.position = list(position)
        self.direction = list(direction)
        self.health = health  
        self.existance = True
        self.shootingSpeed = shootingSpeed
        #0,1 is enemy1, 2,3 enemy2, so on
        self.assets = [transform.scale_by(image.load("basicenemysprite1.png"), 3), transform.scale_by(image.load("basicenemysprite2.png"), 3), transform.scale_by(image.load("enemy2sprite1.png"), 3), transform.scale_by(image.load("enemy2sprite2.png"), 3)]
        self.rect = self.assets[0].get_rect(center = self.position)
        self.frameCounter = 0
        self.currentFrame = 0
        self.cooldown = 0
        self.cooldownLength = 60
        self.orbitRadius = orbitRadius
        self.enemyType = enemyType

    def update(self, playerPosition):
        self.frameCounter += 1
        if self.enemyType == 1:
            if self.frameCounter >= 10:
                self.currentFrame = (self.currentFrame + 1) % 2
                self.frameCounter = 0
        elif self.enemyType == 2:
            if self.frameCounter >= 10:
                self.currentFrame = (self.currentFrame + 1) % 2
                self.frameCounter = 0

        self.playerPosition = playerPosition
        dx = playerPosition[0] - self.position[0]
        dy = playerPosition[1] - self.position[1]
        distance = hypot(dx, dy)

        if distance > self.orbitRadius:
            self.direction = [dx / distance, dy / distance]
            self.position[0] += self.direction[0] * 2
            self.position[1] += self.direction[1] * 2

            self.rect.centerx = self.position[0]
            self.rect.centery = self.position[1]

    def draw(self, screen):
        angle = degrees(atan2(self.playerPosition[1] - self.rect.centery, self.playerPosition[0] - self.rect.centerx)) -90
        self.currentAsset = transform.rotate(self.assets[self.currentFrame+(self.enemyType-1)], -angle)
        self.updatedRect = self.currentAsset.get_rect(center=self.rect.center)
        screen.blit(self.currentAsset, self.updatedRect)


running = True
playerBulletCooldownLength = 60

mainMenuState = True

def mainMenuScreen(mousePos, events):
    global mainMenuState

    menu = transform.scale_by(image.load("menubutton.png"), 5)
    menuRect = menu.get_rect(center=(300, 400))
    startButton = transform.scale_by(image.load("startbutton.png"), 5)
    startButtonRect = startButton.get_rect(center=(500, 400))

    for event in events:
        if event.type == MOUSEBUTTONUP:
            print("Mouse Down")
            if menuRect.collidepoint(mousePos):
                pass
            elif startButtonRect.collidepoint(mousePos):
                print("srjbkjsbf")
                mainMenuState = False

    for button in [[menu, menuRect], [startButton, startButtonRect]]:
        mainscreen.blit(button[0], button[1])


def endScreen(mousePos):
    global player, existingBullets, existingEnemies, running, mainMenuState
    gameOver = transform.scale_by(image.load("gameover.png"), 6)
    gameOverRect = gameOver.get_rect(center=(400, 300))
    quitButton = transform.scale_by(image.load("quitbutton.png"), 5)
    quitButtonRect = quitButton.get_rect(center=(300, 400))
    retryButton = transform.scale_by(image.load("retrybutton.png"), 5)
    retryButtonRect = retryButton.get_rect(center=(500, 400))
    
    if event.type == MOUSEBUTTONDOWN:
        if quitButtonRect.collidepoint(mousePos):
            running = False
        elif retryButtonRect.collidepoint(mousePos):
            player = character((300, 300))
            existingBullets = []
            #self, position, direction, shootingSpeed, health, orbitRadius, enemyType
            existingEnemies = [enemy((random.randrange(0, 700), random.randrange(0, 700)), player.rect.center, 2, 2, 150, 1)]

    for button in [[retryButton, retryButtonRect], [quitButton, quitButtonRect], [gameOver, gameOverRect]]:
            mainscreen.blit(button[0], button[1])
    


player = character((300, 300))
existingBullets = [bullet(player, (0, 0), (0, 0), (0, 0, 0))]
existingEnemies = [enemy((random.randrange(0, 700), random.randrange(0, 700)), player.rect.center, 2, 2, 150, 1)]
pygame.init()

while running:
    ticks = clock.tick(60)
    mainscreen.fill((0,0,0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()

    if mainMenuState:
        mainMenuScreen(mousePos, events)
    
    elif not mainMenuState:
        if player.health == 0:
            endScreen(mousePos)
            
        else:
            if keys[K_LSHIFT]:
                if keys[K_d]:
                    player.rect.centerx += (player.speed/2)
                if keys[K_a]:
                    player.rect.centerx -= (player.speed/2)
                if keys[K_w]:
                    player.rect.centery -= (player.speed/2)
                if keys[K_s]:
                    player.rect.centery += (player.speed/2)
            else:
                if keys[K_d]:
                    player.rect.centerx += player.speed
                if keys[K_a]:
                    player.rect.centerx -= player.speed
                if keys[K_w]:
                    player.rect.centery -= player.speed
                if keys[K_s]:
                    player.rect.centery += player.speed
            
            if player.rect.centerx < 0:
                player.rect.centerx += player.speed
            if player.rect.centerx > 800:
                player.rect.centerx -= player.speed
            if player.rect.centery < 0:
                player.rect.centery += player.speed
            if player.rect.centery > 800:
                player.rect.centery -= player.speed
                

            if keys[K_SPACE] and player.bulletCooldown <= 0:
                mouseX, mouseY = pygame.mouse.get_pos()
                dx, dy = mouseX - player.rect.centerx, mouseY - player.rect.centery
                distance = hypot(dx, dy)

                if distance != 0:
                    direction = [dx / distance, dy / distance]
                    existingBullets.append(bullet(player, player.rect.center, direction, (255, 255, 255 )))
                    player.bulletCooldown = playerBulletCooldownLength

            for bullets in existingBullets:
                if bullets.existance:
                    bullets.update()
                    bullets.draw()

            for enemies in existingEnemies:
                if enemies.health <= 0:
                    enemies.existance = False
                    existingEnemies.remove(enemies)
                    
                if enemies.existance:
                    enemies.update(player.rect.center)
                    enemies.draw(mainscreen)

                    if enemies.cooldown <= 0:
                        dx, dy = player.rect.centerx - enemies.position[0], player.rect.centery - enemies.position[1]
                        distance = hypot(dx, dy)

                        if distance != 0:
                            direction = [dx / distance, dy / distance]
                            existingBullets.append(bullet(enemies, enemies.rect.center, direction, (0, 255, 0)))
                        enemies.cooldown = enemies.cooldownLength
                    else:
                        enemies.cooldown -= enemies.shootingSpeed

                enemiesBullets = []

                for bullets in existingBullets:
                    if bullets.shooter == player:
                        if enemies.rect.colliderect(bullets.visual) and enemies.existance and bullets.existance:
                            bullets.existance = False
                            existingBullets.remove(bullets)
                            enemies.health -= 1
                            if len(existingEnemies) <= 3:
                                newPos = (random.randint(0, 700), random.randint(0, 700))
                                #self, position, direction, shootingSpeed, health, orbitRadius, enemyType
                                if random.randint(0,1) == 0:   
                                    existingEnemies.append(enemy(newPos, player.rect.center, 2, 1, 150, 1))
                                else:
                                    existingEnemies.append(enemy(newPos, player.rect.center, 4, 2, 600, 3))
                                    
                    
                    elif (bullets.shooter in existingEnemies) and player.immunity <= 0:
                        if player.rect.colliderect(bullets.visual) and bullets.existance:
                            print("-1 Health")
                            player.health -= 1
                            bullets.existance = False
                            existingBullets.remove(bullets)
                            player.immunity = 20
            
            if player.immunity > 0:
                player.immunity -= 2

            if player.rect.collidepoint(mousePos):
                playerBulletCooldownLength = 0
            
            
            player.bulletCooldown -= 5
            player.update()
            player.draw()

    pygame.display.flip()
