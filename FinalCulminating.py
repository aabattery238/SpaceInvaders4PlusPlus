import pygame
from pygame import *
from pygame.locals import *
from math import *
import random
# hello
class bullet:
    def __init__(self, speed, coordinates, direction, existance, visual):
        self.speed = speed
        self.coordinates = coordinates
        self.direction = direction
        self.existance = existance
        self.visual = visual

class enemy:
    def __init__(self, existance, coordinates, visual):
        self.existance = existance
        self.coordinates = coordinates
        self.visual = visual

pygame.init()
screen = pygame.display.set_mode((800,800))
color = [(255,0,0),(0,255,0)]
pygame.display.set_caption('im pygaming it')
clock = pygame.time.Clock()
running = True

shot = False

playerX = 300
playerY = 300
speed = 5
defaultBulletSpeed = 10
bulletCooldownLength = 1
bulletCooldown = 0

bulletProperties = bullet(defaultBulletSpeed, 0, [playerX, playerY], False, pygame.draw.circle(screen, (255, 255, 255), (playerX, playerY), 5))
existingBullets = [bulletProperties]

enemyProperties = enemy(True, (400, 400), pygame.draw.circle(screen, (255, 0, 0), (400, 400), 10))
existingEnemies = [enemyProperties]

while running:
    screen.fill((0, 0, 0)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[K_d]:
        playerX += speed
    if keys[K_a]:
        playerX -= speed
    if keys[K_w]:
        playerY -= speed
    if keys[K_s]:
        playerY += speed
    if keys[K_SPACE] and bulletCooldown <= 0:
    
        mouseX, mouseY = pygame.mouse.get_pos()
        dx, dy = mouseX - playerX, mouseY - playerY
        distance = hypot(dx, dy)

        if distance != 0:
            
            print(existingBullets)
            directionX = dx / distance
            directionY = dy / distance
            existingBullets.append(bullet(defaultBulletSpeed, [playerX, playerY], [directionX, directionY], True, pygame.draw.circle(screen, (255, 255, 255), (playerX, playerY), 5)))
            bulletCooldown = bulletCooldownLength

    clock.tick(60)
    bulletCooldown -= 1    
    for enemies in existingEnemies:
        if enemies.existance:
            enemies.visual = pygame.draw.circle(screen, (255, 0, 0), (enemies.coordinates[0], enemies.coordinates[1]), 10)

    for bullets in existingBullets:
        if bullets.existance:
            bullets.coordinates[0] += bullets.direction[0] * bullets.speed                       
            bullets.coordinates[1] += bullets.direction[1] * bullets.speed
            bullets.visual = pygame.draw.circle(screen, (255, 255, 255), (bullets.coordinates[0], bullets.coordinates[1]), 5)
        
        if (enemies.visual).colliderect(bullets.visual):
            bullets.existance = False
            enemies.existance = False          
            newEnemyX = random.randrange(0, 800)
            newEnemyY = random.randrange(0, 800)
            newEnemy = enemy(True, (newEnemyX, newEnemyY), pygame.draw.circle(screen, (255, 0, 0), (newEnemyX, newEnemyY), 10))
            existingEnemies.append(newEnemy)

    character = pygame.draw.circle(screen,(255,0,255),(playerX,playerY),(10),5)
    pygame.display.update()
pygame.quit()
