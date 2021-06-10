import pygame
import random
import math
from pygame import mixer

# Initialise pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('images/background.png')

# background music
mixer.music.load('music/background.wav')
mixer.music.play(-1)

# Title ad icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("images/rocket.png")
pygame.display.set_icon(icon)

# player
player_image = pygame.image.load("images/space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load("images/space-ship.png"))
    enemyX.append(random.randint(0, 771))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
bullet_image = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 20
bullet_state = "ready"

# score font
score_value = 0
font = pygame.font.Font('fonts/Bathrind.otf', 32)
textX = 10
textY = 10

# Game over font
over_font = pygame.font.Font('fonts/Bathrind.otf', 66)


def game_over_text():
    text= """
    Game Over    
    """
    over_text = over_font.render(text, True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Collision detection function
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# bullet firing function
def fire_bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (X + 16, Y + 10))


# enemy function
def enemy(X, Y, i):
    screen.blit(enemy_image[i], (X, Y))


# player function
def player(X, Y):
    screen.blit(player_image, (X, Y))


# Game loop
running = True
while running:
    # screen color
    screen.fill((0, 0, 0))

    # Draw background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # key Checking
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('music/laser.wav')
                    bullet_sound.play()
                    # get the x coordinate of the space ship
                    bulletX = playerX
                    fire_bullet(int(bulletX), int(bulletY))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # player window boundary

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy window boundary
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 772:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]

        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('music/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 771)
            enemyY[i] = random.randint(50, 150)
        enemy(int(enemyX[i]), int(enemyY[i]), i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(int(bulletX), int(bulletY))
        bulletY -= bulletY_change

    player(int(playerX), int(playerY))
    show_score(textX, textY)
    pygame.display.update()
