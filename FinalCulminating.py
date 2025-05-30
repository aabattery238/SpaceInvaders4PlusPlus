import pygame
from pygame import *
from pygame.locals import *
import random
from math import *


bulletRadius = 5
enemyRadius = 10

class bullet:
    def __init__(self, position, direction, speed, existance):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.existance = existance
        self.rect = pygame.Rect(self.position[0], self.position[1], bulletRadius*2, bulletRadius*2)

    def update(self):
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
        self.rect.topleft = (self.position[0], self.position[1])
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position[0]), int(self.position[1])), bulletRadius)

class enemy:
    def __init__(self, position, existance):
        self.position = position
        self.existance = existance
        self.rect = pygame.Rect(self.position[0] - enemyRadius, self.position[1] - enemyRadius, enemyRadius*2, enemyRadius*2)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position, enemyRadius)

pygame.init()
playerPosition = [300, 300]
bulletCooldownLength = 1
bulletCooldown = 0
playerSpeed = 5
defaultBulletSpeed = 10
clock = pygame.time.Clock()
mainscreen = pygame.display.set_mode((800,800))
existingBullets = [bullet(playerPosition, [0, 0], defaultBulletSpeed, False)]
existingEnemies = [enemy((400, 400), True)]
running = True

#Assets
characterAsset = pygame.image.load("playersprite1.png")
characterRect = characterAsset.get_rect(center=(400, 400))

while running:
    clock.tick(60)
    mainscreen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    if keys[K_a]:
        playerPosition[0] += playerSpeed
    if keys[K_a]:
        playerPosition[0] -= playerSpeed
    if keys[K_a]:
        playerPosition[1] -= playerSpeed
    if keys[K_a]:
        playerPosition[1] += playerSpeed

    if keys[K_SPACE] and bulletCooldown <= 0:
        mouseX, mouseY = pygame.mouse.get_pos()
        dx, dy = mouseX - playerPosition[0], mouseY - playerPosition[1]
        distance = hypot(dx, dy)
        
        if distance != 0:
            direction = [dx / distance, dy / distance]
            existingBullets.append(bullet(playerPosition, direction, defaultBulletSpeed, True))
            bulletCooldown = bulletCooldownLength

    for bullets in existingBullets:
        bullets.update()
        bullets.draw(mainscreen)

    for enemies in existingEnemies:
        enemy.draw(enemies, mainscreen)
        
        for bullets in existingBullets:
            if enemies.rect.colliderect(bullets.rect) and enemies.existance and bullets.existance:
                bullets.existance = False
                enemies.existance = False
                existingBullets.remove(bullets)
                existingEnemies.remove(enemies)
                newPos = (random.randint(0, 800), random.randint(0, 800))
                existingEnemies.append(enemy(newPos, True))
                break
            
    bulletCooldown -= 0.1

    characterRect.center = [1, 1]
    mainscreen.blit(characterAsset, characterRect)

    pygame.display.flip()

pygame.quit()
