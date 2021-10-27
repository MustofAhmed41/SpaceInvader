import pygame
import random
import math
from pygame import mixer  # music

# ctrl + alt + L to auto format

# intializing pygame and we must do it every time at first
pygame.init()

# creating screen
screen = pygame.display.set_mode((800, 600))  # width and height
# The width and height starts from top left and as it goes right X increases (width)
# As is goes down the value of Y increases (height)


# music
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 as parameter implies run the music infinitely
# as we want to run the background music always we are putting it here

# Title and Icon
pygame.display.set_caption("Space Invaders")

# Background
background = pygame.image.load('background.png')

# importing image in our game
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)  # This is the icon for our game which will be on upper tab

# Player Image
playerImg = pygame.image.load('playerImage.png')
playerX = 370
playerY = 480
playerX_change = 0  # this value is the amount of change made to playerX and playerY

# Enemy enemies information will be stored here so using array
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):  # Initializing all the values of the enemies at beginning
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 734))  # The enemy will spawn at a random position initially
    enemyY.append(random.randint(50, 150))  # This means random value between 50 and 150
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# ready - you can't see the bullet on the screen
# fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0  # x coordinate of bullet remains unchanged
bulletY_change = 10  # y changes and is dependent on this variable
bullet_state = "ready"  # Initially it is in ready state so that we can fire it

# SCORE
score_value = 0  # its an built in font and available in pycharm/pygame and .tff is extension and 32 is size of the font
# importing the font we are going to use at first and placing it in a variable
font_name = pygame.font.Font('freesansbold.ttf', 32)  # To use different font go to dafont.com and download the zip file,
textX = 10  # extract it and put it in the project folder like the image and put the font name here in the previous line
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64) # setting font for game over


def game_over_text(): # This is called when any of the enemies goes beyond a certain limit of Y
    over_text = over_font.render("Game Over ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))  # This bit of code is one responsible for displaying text on screen


def show_score(x, y):
    score = font_name.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):  # image of player
    screen.blit(playerImg, (x, y))  # blit means to draw on screen


def enemy(x, y, i):  # image of player
    screen.blit(enemyImg[i], (x, y))  # blit means to draw on screen


def fire_bullet(x, y):  # This is called whenever spacebar is hit
    global bullet_state  # This refers accessing the global bullet_state and making any changes here changes the actual bullet_state
    bullet_state = "fire"  # While it is in fire state the rendering is true in running loop and the bullet is displayed
    screen.blit(bulletImg,
                (x + 16, y + 10))  # adjusting bullet position so that it appears to come out of front of the plane


def isCollision(enemyX, enemyY, bulletX, bulletY):  # Figuring out whether collision occurred or not
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:   # using mathematics formula of coordinate geometry to find out the distance
        return True
    else:
        return False


# This will keep the screen running or else the screen executes immediately
running = True
# Game loop
while running:

    screen.fill((0, 0, 0))  # R G B This must always be at top or it will
    # be drawn later over other parts hide them behind

    screen.blit(background, (0, 0))  # This is the background rendering
    # This background image is very heavy which decreases the rendering of other enemies and
    # players so we have to increase the speed of enemy and player accordingly

    for event in pygame.event.get():  # this will capture every event that occurs
        if event.type == pygame.QUIT:  # when the cross button of top right of the
            running = False  # screen window is pressed this will be executed

        if event.type == pygame.KEYDOWN:  # This is called whenever a key is pressed DOWN
            print("A key has been pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5  # amount of change in x when left button pressed
            if event.key == pygame.K_RIGHT:
                playerX_change = 5  # amount of change in x when right button pressed
            if event.key == pygame.K_SPACE:  # Firing Bullet
                if bullet_state == "ready":  # If we don't give this then there will be error in rendering the bullet
                    bulletX = playerX  # Doing this so that the bullet doesn't move along x axis as we change the value x of player
                    fire_bullet(bulletX, bulletY)  # showing bullet image here

                    bullet_Sound = mixer.Sound('laser.wav') # this one is sound rather than music because we want to
                    bullet_Sound.play() # only play it once not infinitely unlike background music

        if event.type == pygame.KEYUP:  # This is called whenever a key is lifted up after pressing down
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # if we don't give this then the playerX keeps on changing which goes out of our control

    playerX += playerX_change
    if playerX <= 0:  # Boundary condition checking
        playerX = 0
    elif playerX >= 736:  # since size of pic is 64. Hence 800-64 = 736 is exact
        playerX = 736

    # checking boundaries for enemy space ship

    for i in range(num_of_enemies):  # rendering of all enemies movements

        if enemyY[i] > 440:  # Here we are checking the game over condition if any of the enemies crossed a certain
            for j in range(num_of_enemies):  # y - axis
                enemyY[j] = 2000  # removing the enemies from screen by pushing it down
            game_over_text()  # game over text being called
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # Boundary condition checking of enemies
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]  # moves down every time enemy hits the walls
        elif enemyX[i] >= 736:  # since size of pic is 64. Hence 800-64 = 736 is exact
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision for all enemies
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"  # re-setting bullet to player again
            score_value += 1
            enemyX[i] = random.randint(0, 734)  # re-setting enemy position after it died
            enemyY[i] = random.randint(50, 150)
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()

        enemy(enemyX[i], enemyY[i], i)  # updating enemy info of index i

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"  # Readying it so that we can fire again after it leaves the screen from top or else we wouldn't be able to
    if bullet_state == "fire":  # changing value of bullet while it is on fire state
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)  # we want the score to be displayed always so it is here
    pygame.display.update()  # we must call it always because the line above alone
    # doesn't mean anything and we must put it on screen so must call the line above
    # since we are doing something continuously we must put it in running loop
