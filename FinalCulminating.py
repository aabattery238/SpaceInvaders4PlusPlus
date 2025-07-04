import pygame
from pygame import *
from pygame.locals import *
import random
from math import *


#Sets Level details
levelproperties = {
    # waves = number of waves
    # enemies/wave = the number of enemies spawn for each wave
    # enemiesChance = chance of which enemy type spawns
    1 : {
        "waves" : 1,
        "enemies/wave" : 4,
        "enemiesChance" : 0
    },
    2 : {
        "waves" : 3,
        "enemies/wave" : 6,
        "enemiesChance" : 1
    },
    3 : {
        "waves" : 3,
        "enemies/wave" : 8,
        "enemiesChance" : 3
    },
    4 : {
        "waves" : 1,
        "enemies/wave" : 10,
        "enemiesChance" : 10
    }
}

#Initialize Clock
clock = pygame.time.Clock()
#Initialize Screen
mainscreen = pygame.display.set_mode((800,800))
#Initialize Sound PEW
pygame.mixer.init()
pewSound = pygame.mixer.Sound("pew.mp3")
pewSound.set_volume(0.5)

class character:
    #Initialize Player Class
    def __init__(self, position):
        #immunity value
        self.immunity = 0
        #Health Start
        self.health = 5
        #Position Inputed
        self.position = tuple(position)
        #Assets to animate
        self.assets = [transform.scale_by(image.load("playersprite1.png"), 3), transform.scale_by(image.load("playersprite2.png"), 3)]
        #Rectangle/Boundry
        self.rect = self.assets[0].get_rect(center = self.position)
        self.frameCounter = 0
        self.currentFrame = 0
        self.bulletCooldown = 0
        #Player Speed
        self.speed = 5
        self.points = 0
        #Ticks between New Bullet 
        self.bulletCooldownLength = 60
        #Power Up Stuff
        self.teleport = False
        self.teleporting = False
        self.laserMode = False
        self.laserModeImage = False
        self.laserTimer = 0
        self.powerUpCooldown = 0
        self.powerUpCooldownLength = 320

    def update(self):
        #Update the Frame of Class Character
        self.frameCounter += 1
        if self.frameCounter >= 10:
            self.currentFrame = (self.currentFrame + 1) % len(self.assets)
            self.frameCounter = 0

    def draw(self):
        #Draw the Image based on scaling, and rotation 
        if self.teleporting:
            self.currentAsset = transform.rotate(transform.rotate(transform.scale_by(image.load("playerspriteteleport.png"), 3), -player.angle), -self.angle)
            self.updatedRect = self.currentAsset.get_rect(center=self.rect.center)
            mainscreen.blit(self.currentAsset, self.updatedRect)

        elif self.laserModeImage:
            #Change image for if laser powerup is active
            self.laserAssets = [transform.scale_by(image.load("playerspritelaser1.png.png"), 3), transform.scale_by(image.load("playerspritelaser2.png.png"), 3)]
            self.frameCounter += 1
            if self.frameCounter >= 10:
                self.currentFrame = (self.currentFrame + 1) % len(self.laserAssets)
                self.frameCounter = 0
            mouseX, mouseY = pygame.mouse.get_pos()
            self.angle = degrees(atan2(mouseY - self.rect.centery, mouseX - self.rect.centerx)) + 90
            self.currentAsset = transform.rotate(self.laserAssets[self.currentFrame], -self.angle)
            self.updatedRect = self.currentAsset.get_rect(center=self.rect.center)
            mainscreen.blit(self.currentAsset, self.updatedRect)
        else:
            #Angle rotation math
            mouseX, mouseY = pygame.mouse.get_pos()
            self.angle = degrees(atan2(mouseY - self.rect.centery, mouseX - self.rect.centerx)) + 90
            self.currentAsset = transform.rotate(self.assets[self.currentFrame], -self.angle)
            self.updatedRect = self.currentAsset.get_rect(center=self.rect.center)
            mainscreen.blit(self.currentAsset, self.updatedRect)

class bullet():
    #Initialize Bullet Class
    def __init__(self, shooter, position, direction, colour):
        #Who is shooting Enemy or Player
        self.shooter = shooter
        self.position = list(position)
        self.direction = list(direction)
        self.colour = tuple(colour)
        self.existance = True
        self.visual = draw.circle(mainscreen, self.colour, self.position, 5)

    def update(self):
        #Move towards target different speeds based on shooter
        if type(self.shooter) == character:
            self.position[0] += self.direction[0] * 10
            self.position[1] += self.direction[1] * 10
        else:
            self.position[0] += self.direction[0] * 5
            self.position[1] += self.direction[1] * 5

    def draw(self):
        #Draw bullet each tick
        self.visual = pygame.draw.circle(mainscreen, self.colour, self.position, 5)
        


class enemy:
    #Initialize Enemy Class
    def __init__(self, position, direction, shootingSpeed, health, orbitRadius, enemyType, pointValue):
        self.position = list(position)
        #Enemy Target
        self.direction = list(direction)
        #health each enemy has
        self.health = health  
        self.existance = True
        self.shootingSpeed = shootingSpeed
        #0 is enemy 1, 1 is enemy 2, you know the drill
        self.assets = [[transform.scale_by(image.load("basicenemysprite1.png"), 3), transform.scale_by(image.load("basicenemysprite2.png"), 3)], 
                       [transform.scale_by(image.load("enemy2sprite1.png"), 3), transform.scale_by(image.load("enemy2sprite2.png"), 3)], 
                       [transform.scale_by(image.load("boss1sprite1.png"), 2), transform.scale_by(image.load("boss1sprite2.png"), 2)], 
                       [transform.scale_by(image.load("boss2sprite1.png"), 0.3), transform.scale_by(image.load("boss2sprite2.png"), 0.3)]]
        self.rect = self.assets[0][0].get_rect(center = self.position)
        self.frameCounter = 0
        self.currentFrame = 0
        self.cooldown = 0
        self.cooldownLength = 60
        #distance where enemy orbits
        self.orbitRadius = orbitRadius
        self.enemyType = enemyType
        self.pointValue = pointValue

    def update(self, playerPosition):
        #update frame based on enemy
        self.frameCounter += 1
        if self.frameCounter >= 10:
            if self.enemyType in [0, 1, 2, 3]:
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
        #draw enemy based on type and change angle depending on where player is
        angle = degrees(atan2(self.playerPosition[1] - self.rect.centery, self.playerPosition[0] - self.rect.centerx)) -90
        self.currentAsset = transform.rotate(self.assets[self.enemyType][self.currentFrame], -angle)
        self.updatedRect = self.currentAsset.get_rect(center=self.rect.center)
        screen.blit(self.currentAsset, self.updatedRect)

class powerUp:
    #initialize powerups
    def __init__(self, type, position):
        self.position = position
        self.type = type
        #Power up options
        if self.type == "teleport":
            self.image = transform.scale_by(image.load("teleporticon.png"), 3)
        elif self.type == "health":
            self.image = transform.scale_by(image.load("healthboosticon.png"), 3)
        elif self.type == "laser":
            self.image = transform.scale_by(image.load("lasericon.png"), 3)
    
    def draw(self, screen):
        #Draw powerup based on asset
        self.rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, self.rect)
        

running = True

mainMenuState = True
helpMenuState = False

def helpScreen():
    #function to draw help screen
    global mainMenuState, helpMenuState
    controlsAsset = transform.scale_by(image.load("controls.png"), 4)
    controlsRect = controlsAsset.get_rect(center=(400, 300))
    menu = transform.scale_by(image.load("menubutton.png"), 4)
    menuRect = menu.get_rect(center = (400, 600))
    if event.type == MOUSEBUTTONDOWN:
        if menuRect.collidepoint(mousePos):
            helpMenuState = False
            mainMenuState = True
    for button in [[controlsAsset, controlsRect], [menu, menuRect]]:
            mainscreen.blit(button[0], button[1])


def mainMenuScreen(mousePos):
    #function to draw menu screen
    global mainMenuState, running, helpMenuState
    startButton = transform.scale_by(image.load("startbutton.png"), 5)
    startButtonRect = startButton.get_rect(center=(400, 300))
    quitButton = transform.scale_by(image.load("quitbutton.png"), 5)
    quitButtonRect = quitButton.get_rect(center=(300, 400))
    helpButton = transform.scale_by(image.load("helpbutton.png"), 5)
    helpButtonRect = helpButton.get_rect(center=(500, 400))
    titleCard = transform.scale_by(image.load("titlecard.png"), 4)
    titleCardRect = titleCard.get_rect(center=(400, 150))
    

    if event.type == MOUSEBUTTONUP:
        if startButtonRect.collidepoint(mousePos):
            mainMenuState = False
        elif quitButtonRect.collidepoint(mousePos):
            running = False
        elif helpButtonRect.collidepoint(mousePos):
            helpMenuState = True
            mainMenuState = False
            helpScreen()

    for button in [[startButton, startButtonRect],[quitButton, quitButtonRect],[helpButton,helpButtonRect], [titleCard, titleCardRect]]:
        mainscreen.blit(button[0], button[1])


def endScreen(mousePos):
    #function to draw end screen
    global player, existingBullets, existingEnemies, running, mainMenuState, level, wave, levelUpPowerUp
    levelUpPowerUp = []
    level = 1
    wave = 0
    menu = transform.scale_by(image.load("menubutton.png"), 4)
    menuRect = menu.get_rect(center=(400, 500))
    gameOver = transform.scale_by(image.load("gameover.png"), 6)
    gameOverRect = gameOver.get_rect(center=(400, 200))
    quitButton = transform.scale_by(image.load("quitbutton.png"), 5)
    quitButtonRect = quitButton.get_rect(center=(300, 400))
    retryButton = transform.scale_by(image.load("retrybutton.png"), 5)
    retryButtonRect = retryButton.get_rect(center=(500, 400))
    font = pygame.font.Font('pixeloid.ttf',40)
    finalPoints = font.render("Final Score: "+str(player.points),True,(255,255,255),(0,0,0))
    finalPointsRect = finalPoints.get_rect(center=(400,300))


    if event.type == MOUSEBUTTONDOWN:
        if quitButtonRect.collidepoint(mousePos):
            running = False
        elif retryButtonRect.collidepoint(mousePos):
            player = character((300, 300))
            existingBullets = []
            #self, position, direction, shootingSpeed, health, orbitRadius, enemyType
            existingEnemies = [enemy((random.randrange(0, 700), random.randrange(0, 700)), player.rect.center, 2, 2, 150, 0, 1)]
        elif menuRect.collidepoint(mousePos):
            mainMenuState = True
            player = character((300, 300))
            existingBullets = []
            #self, position, direction, shootingSpeed, health, orbitRadius, enemyType
            existingEnemies = [enemy((random.randrange(0, 700), random.randrange(0, 700)), player.rect.center, 2, 2, 150, 0, 1)]

    for button in [[retryButton, retryButtonRect], [quitButton, quitButtonRect], [gameOver, gameOverRect], [menu, menuRect],[finalPoints, finalPointsRect]]:
            mainscreen.blit(button[0], button[1])


def healthDisplay():
    #function to draw health counter
    heart = transform.scale_by(image.load("heart.png"), 4)
    heartRect = heart.get_rect(center=(25,25))
    font = pygame.font.Font('pixeloid.ttf',40)
    healthDisplayNumber = font.render(str(player.health),True,(255,255,255),(0,0,0))
    healthDisplayRect = healthDisplayNumber.get_rect(center=(60,25))
    for button in [[heart, heartRect], [healthDisplayNumber, healthDisplayRect]]:
            mainscreen.blit(button[0], button[1])

#create player Character
player = character((300, 300))
#List of existing bullets
existingBullets = [bullet(player, (0, 0), (0, 0), (0, 0, 0))]
#List of existing enemies
existingEnemies = [enemy((random.randrange(0, 800), random.randrange(0, 300)), player.rect.center, 2, 1, 150, 0, 1)]
level = 1
wave = 0
#list of existing powerups
levelUpPowerUp = []
pygame.init()

#run pygame screen
while running:
    #Colock tick 60 per second
    ticks = clock.tick(60)
    #fill screen with black to erase previous frame before new one
    mainscreen.fill((0,0,0))
    #get events like keyboard click
    events = pygame.event.get()
        #quit pygame
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    #list of key values
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()
    #first time loading or death display menu
    if mainMenuState:
        mainMenuScreen(mousePos)
    
    elif not mainMenuState:
        #display help if help clicked
        if helpMenuState:
            helpScreen()
        elif not helpMenuState:
            #End game if health is 0
            if player.health == 0:
                endScreen(mousePos)
            
            else:
                #game
                if keys[K_LSHIFT]:
                    #crouching --> reduce speed
                    if keys[K_d]:
                        player.rect.centerx += (player.speed/2)
                    if keys[K_a]:
                        player.rect.centerx -= (player.speed/2)
                    if keys[K_w]:
                        player.rect.centery -= (player.speed/2)
                    if keys[K_s]:
                        player.rect.centery += (player.speed/2)
                else:
                    #regular speed
                    if keys[K_d]:
                        player.rect.centerx += player.speed
                    if keys[K_a]:
                        player.rect.centerx -= player.speed
                    if keys[K_w]:
                        player.rect.centery -= player.speed
                    if keys[K_s]:
                        player.rect.centery += player.speed
                #border check
                if player.rect.centerx < 0:
                    player.rect.centerx += player.speed
                if player.rect.centerx > 800:
                    player.rect.centerx -= player.speed
                if player.rect.centery < 0:
                    player.rect.centery += player.speed
                if player.rect.centery > 800:
                    player.rect.centery -= player.speed
                    

                if keys[K_SPACE] and player.bulletCooldown <= 0:
                    #create bullet if space clicked
                    mouseX, mouseY = pygame.mouse.get_pos()
                    dx, dy = mouseX - player.rect.centerx, mouseY - player.rect.centery
                    distance = hypot(dx, dy)

                    if distance != 0:
                        direction = [dx / distance, dy / distance]
                        #play pew sound
                        pewSound.play()
                        existingBullets.append(bullet(player, player.rect.center, direction, (255, 255, 255 )))
                        player.bulletCooldown = player.bulletCooldownLength

                for bullets in existingBullets:
                    #draw all valid bullets
                    if bullets.existance:
                        bullets.update()
                        bullets.draw()

                for enemies in existingEnemies:
                    #draw all valid enemies
                    if enemies.health <= 0:
                        #delete dead enemies
                        player.points += enemies.pointValue
                        enemies.existance = False
                        existingEnemies.remove(enemies)
                        
                    if enemies.existance:
                        #point enemy towards player
                        enemies.update(player.rect.center)
                        enemies.draw(mainscreen)

                        if enemies.cooldown <= 0:
                            #enemy shooting cool down
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
                            #remove enemy health if player bullet hits
                            if enemies.rect.colliderect(bullets.visual) and enemies.existance and bullets.existance:
                                bullets.existance = False
                                existingBullets.remove(bullets)
                                enemies.health -= 1
                                if enemies.enemyType == 3:
                                    #Secret Boss fight
                                    for x in range(0, 3):
                                        newPos = (random.randint(100, 700), random.randint(0, 400))
                                        enemySpawnType = random.randint(0, 10)
                                        if enemySpawnType == 1:
                                            existingEnemies.append(enemy(newPos, player.rect.center, 4, 2, 600, 1, 3))
                                        elif enemySpawnType == 2:
                                            existingEnemies.append(enemy(newPos, player.rect.center, 1, 5, 20, 2, 10))
                                        else:
                                            existingEnemies.append(enemy(newPos, player.rect.center, 2, 1, 150, 0, 1))
                
                        elif (bullets.shooter in existingEnemies) and player.immunity <= 0:
                            if player.rect.colliderect(bullets.visual) and bullets.existance:
                                player.health -= 1
                                mainscreen.fill((255,0,0))
                                bullets.existance = False
                                existingBullets.remove(bullets)
                                player.immunity = 30
                    


                if len(existingEnemies) <= 0: #when enmies are all defeated create a new wave
                    levels = list(levelproperties.keys())
                    if wave >= levelDetails["waves"]: #if all the waves have been defeated create new level
                        if level + 1 in levels:
                            print("LEVEL INCREASED")
                            level += 1
                        else:
                            print("MAX LEVEL REACHED OR INVALID LEVEL")
                        levelUpPowerUp.clear() #clear all un picked powerups
                        power = random.choice(["teleport", "health", "laser"])
                        levelUpPowerUp.append(powerUp(power, (random.randint(200, 700), random.randint(200, 300))))
                        for powers in levelUpPowerUp:
                            powers.draw(mainscreen)
                        wave = 0 #reset wace counter
                        existingEnemies.clear()
                
                    #self, position, direction, shootingSpeed, health, orbitRadius, enemyType
                    if levelDetails["enemiesChance"] == 10 and random.randrange(0, 4) == 0: #create boss when level 4 reached + random chance
                            existingEnemies.clear()
                            existingEnemies.append(enemy((400, 100), player.rect.center, 60, 20, 800, 3, 100))
                            level -= 1

                    else: #if not boss create regular enemies based on enemies/wave and chance
                        while len(existingEnemies) < levelDetails["enemies/wave"]:
                            newPos = (random.randint(100, 700), random.randint(0, 400))
                            enemySpawnType = random.randint(0,levelDetails["enemiesChance"])
                            if enemySpawnType == 1:
                                existingEnemies.append(enemy(newPos, player.rect.center, 4, 2, 600, 1, 3))
                            elif enemySpawnType == 2:
                                existingEnemies.append(enemy(newPos, player.rect.center, 1, 5, 20, 2, 10))
                            else:
                                existingEnemies.append(enemy(newPos, player.rect.center, 2, 1, 150, 0, 1))
                    wave += 1
                    player.immunity = 40
                    existingBullets = []

                levelDetails = levelproperties[level]

                if player.immunity > 0: #player immunity
                    player.immunity -= 1

                if keys[K_o] and keys[K_p]: #OP mode for Abdullah and Derek ONLY not Mr. Nagra
                    player.health = 100000
                    player.bulletCooldownLength = 0
                    player.laserTimer = 10000000000000000000
                    player.teleport = True
                    player.powerUpCooldownLength = 0

                if keys[K_l]: #Enemy spawner FOR TESTING ONLY ;)
                    newPos = (random.randint(100, 700), random.randint(0, 400))
                    enemySpawnType = random.randint(0, 10)
                    if enemySpawnType == 1:
                        existingEnemies.append(enemy(newPos, player.rect.center, 4, 2, 600, 1, 3))
                    elif enemySpawnType == 2:
                        existingEnemies.append(enemy(newPos, player.rect.center, 1, 5, 20, 2, 10))
                    else:
                        existingEnemies.append(enemy(newPos, player.rect.center, 2, 1, 150, 0, 1))

                if keys[K_n]: #Boss spawner FOR TESTING ONLY ;)
                    newPos = (random.randint(100, 700), random.randint(0, 400))
                    existingEnemies.append(enemy((400, 100), player.rect.center, 60, 20, 800, 3, 100))
                
                for powers in levelUpPowerUp:
                    #powerups!
                    powers.draw(mainscreen)
                    if player.rect.colliderect(powers.rect):
                        if powers.type == "teleport":
                            player.teleport = True
                            levelUpPowerUp.remove(powers)
                        elif powers.type == "health":
                            player.health += random.randrange(1, 4)
                            levelUpPowerUp.remove(powers)
                        elif powers.type == "laser":
                            player.laserMode = True
                            levelUpPowerUp.remove(powers)
                            
                if random.randrange(0, 10000) == 0: #randomly spawn health
                    levelUpPowerUp.append(powerUp("health", (random.randint(200, 700), random.randint(200, 300))))

                if player.powerUpCooldown <= 0: #Teleport
                    if keys[K_c] and player.teleport:
                        player.teleporting = True
                        player.powerUpCooldown = player.powerUpCooldownLength
                        player.rect.center = mousePos

                    elif keys[K_f] and player.laserMode: #laser
                        player.laserTimer = 60
                        player.laserModeImage = True
                        player.draw()
                        player.powerUpCooldown = player.powerUpCooldownLength
                
                if player.laserTimer > 0: #laser timer
                    player.bulletCooldownLength = 0
                else:
                    player.bulletCooldownLength = 60
                    player.laserModeImage = False

                player.laserTimer -= 1 #laser timer remander
                player.bulletCooldown -= 5 #Player bullet cooldown 
                player.powerUpCooldown -= 1 #powerup cooldown to use new powerup
                healthDisplay() #display health
                player.update() #draw and update player
                player.draw()
                player.teleporting = False #stop player teleporting afterwards


    pygame.display.flip()
