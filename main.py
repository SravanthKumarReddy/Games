import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1080, 720))
background = pygame.image.load("background.jpeg")

mixer.music.load("mixkit-mystwrious-bass-pulse-2298.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Defence")
game_Icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(game_Icon)

# player
player_image = pygame.image.load("playerShip.png")
playerx = 500
playery = 550
playerx_position = 0
playery_position = 0

# villain 1
villain_icon = []
villainx = []
villainy = []
villain_position_x = []
villain_position_y = []
number_of_villains = 5
for i in range(number_of_villains):
    villain_icon.append(pygame.image.load("monster.png"))
    villainx.append(random.randint(0, 1048))
    villainy.append(random.randint(50, 200))
    villain_position_x.append(0.5)
    villain_position_y.append(0)

# villain 2
villain_icon2 = []
villain2x = []
villain2y = []
villain_position_2x = []
villain_position_2y = []
for i in range(number_of_villains):
    villain_icon2.append(pygame.image.load("alien.png"))
    villain2x.append(random.randint(0, 1048))
    villain2y.append(random.randint(50, 200))
    villain_position_2x.append(0.5)
    villain_position_2y.append(0)


# laser
laser_icon = pygame.image.load("Laser.png")
laserx = 0
lasery = 550
laser_position_x = 0
laser_position_y = 5
laser_state = "ready"

score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
testx = 10
testy = 10

final_words = pygame.font.Font("Nightcore Demo.ttf", 80)


def show_score(x, y):
    score_value = font.render("score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def game_over():
    final_word_value = final_words.render(
        "You have been Defeated!", True, (255, 255, 255)
    )
    screen.blit(final_word_value, (150, 360))


def player(x, y):
    screen.blit(player_image, (x, y))


def villain(x, y, i):
    screen.blit(villain_icon[i], (x, y))

def villain2(x, y, i):
    screen.blit(villain_icon2[i], (x, y))


def laser_fire(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laser_icon, (x + 20, y + 20))


def collision(villainx, villainy, laserx, lasery):
    distance = math.sqrt(
        (math.pow(villainx - laserx, 2)) + (math.pow(villainy - lasery, 2))
    )
    if distance < 16:
        return True
    else:
        return False

def collision2(villain2x, villain2y, laserx, lasery):
    distance = math.sqrt(
        (math.pow(villain2x - laserx, 2)) + (math.pow(villain2y - lasery, 2))
    )
    if distance < 16:
        return True
    else:
        return False

running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_position = -1
            if event.key == pygame.K_UP:
                playery_position = -1
            if event.key == pygame.K_DOWN:
                playery_position = 1
            if event.key == pygame.K_RIGHT:
                playerx_position = 1
            if event.key == pygame.K_SPACE:
                laser_sound = mixer.Sound("laser.wav")
                laser_sound.play()
                laserx = playerx
                laser_fire(laserx, lasery)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playery_position = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_position = 0
    playery += playery_position
    if playery < 450:
        playery = 450
    elif playery >=550:
        playery = 550
        
    playerx += playerx_position
    if playerx < 0:
        playerx = 0
    elif playerx >= 1016:
        playerx = 1016
    for i in range(number_of_villains):
        if villainy[i] > 500 or villain2y[i]>500:
            for j in range(number_of_villains):
                villainy[j] = 2000
                villain2y[j] = 2000
            game_over()
            break
        villainx[i] += villain_position_x[i]
        if villainx[i] < 0:
            villainx[i] = 0
            villain_position_x[i] = 0.5
            if villainx[i] == 0:
                villainy[i] += 50
        elif villainx[i] >= 1048:
            villainx[i] = 1048
            villain_position_x[i] = -0.5
            if villainx[i] == 1048:
                villainy[i] += 50
        villain2x[i] += villain_position_2x[i]
        if villain2x[i] < 0:
            villain2x[i] = 0
            villain_position_2x[i] = 0.5
            if villain2x[i] == 0:
                villain2y[i] += 50
        elif villain2x[i] >= 1048:
            villain2x[i] = 1048
            villain_position_2x[i] = -0.5
            if villain2x[i] == 1048:
                villain2y[i] += 50
        collis = collision(villainx[i], villainy[i], laserx, lasery)
        if collis:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            lasery = 550
            laser_state = "ready"
            score += 1
            villainx[i] = random.randint(0, 1048)
            villainy[i] = random.randint(50, 200)
        villain(villainx[i], villainy[i], i)
        colli = collision2(villain2x[i], villain2y[i], laserx, lasery)
        if colli:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            lasery = 550
            laser_state = "ready"
            score += 1
            villain2x[i] = random.randint(0, 1048)
            villain2y[i] = random.randint(50, 200)
        villain2(villain2x[i], villain2y[i], i)
            
    if lasery <= 0:
        lasery = 550
        laser_state = "ready"
    if laser_state is "fire":
        laser_fire(laserx, lasery)
        lasery -= laser_position_y

    player(playerx, playery)
    show_score(testx, testy)
    pygame.display.update()
