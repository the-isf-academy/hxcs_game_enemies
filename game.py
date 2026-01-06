# /////////// INFO /////////////////
#
# 👾 This game has a shooting mechanic and moving enemies 👾
#
# 1️⃣ Run the file & install
#    - in the Terminal run the commands: 
#.          python3 -m venv my_project_env
#           source my_project_env/bin/activate
#           pip3 install pgzero
#
# 💻  You need to fix the following
#  - enemies should move the full width of the screen
#  - enemies should randomly spawn all over the screen
#  - bullets should move faster
#  - score should increase
#  - timer less than 0 should end the game
#
# 📖 Offical Documentation
#      - https://pygame-zero.readthedocs.io
#      - https://pygame-zero.readthedocs.io/en/stable/ptext.html
#            - how to customize text
#      - https://quirkycort.github.io/tutorials/20-Pygame-Zero-Basics/10-Intro/10-intro.html
#
# ////////////////////////////////////////////

import pgzrun
from helpers import *
import random
import sys

### 🎛 Controls game settings

# Setup the Screen Size
WIDTH = 600
HEIGHT = 600

# Setup the background image
background = Actor("water.jpeg")

# Setup the player
player = Actor("square_man.png", anchor=("center", "middle"))
player.scale = 2  # scales the sprite image
player.x = WIDTH/2  # sets the X position
player.y = HEIGHT - 50 # sets the Y position
player.velocityX = 5
player.velocityY = 5


# Sets up enemies
enemy_list = []

for i in range(2):
    enemy = Actor("alien.png")
    enemy.scale = 1
    enemy.y = 100
    enemy.x = random.randint(100, 300)
    enemy.velocityX = 1
    enemy_list.append(enemy)

# Setup tracking if game is running
game_running = True

# Setup score
score = 0

# Setup timer
timer = 20

# Sets up bullet_list
bullet_list = []
bullet_countdown = 0  

def draw():

    if game_running == True:
        background.draw()

        screen.draw.text(f"Score: {str(score)}", centerx=WIDTH / 2, centery=HEIGHT / 6)
        screen.draw.text(f"Time Left: {round(timer,1)}s", centerx=WIDTH / 2, centery=HEIGHT / 8)

        player.draw()

        for enemy in enemy_list:
            enemy.draw()

        for bullet in bullet_list:
            bullet.draw()

    else:
        screen.fill((149, 161, 171))

        screen.draw.text(f"Score: {str(score)}", centerx=WIDTH / 2, centery=HEIGHT / 6)
        screen.draw.text(f"GAME OVER", centerx=(WIDTH / 2) + 100, centery=HEIGHT / 2)

def key_presses():
    global game_running, bullet_countdown
    
    if keyboard.a:
        player.x -= player.velocityX
        player.flip_x = True

    if keyboard.d:
        player.x += player.velocityX
        #player.flip_x = False

    if keyboard[keys.ESCAPE]:
        sys.exit()

    # creates bullet if space bar is pressed and recoil time has elapsed
    if bullet_countdown == 0:
        if keyboard[keys.SPACE]:

            bullet = Actor('laser_sprite.png', anchor=("center", "middle"))
            bullet.scale = 0.05
            bullet.angle = 90
            bullet.x = player.x         # bullet spawn X 
            bullet.y = player.y + 20    # bullet spawn Y
            bullet.velocityY = 1        # bullet movement speed
            bullet_list.append(bullet)
            bullet_countdown = 30       # recoil time of bullet 
    else:
        bullet_countdown -= 1

def enemy_movement():
    global game_running 

    # controls enemy movement
    for enemy in enemy_list:
        enemy.x += enemy.velocityX

        # limits of enemy horizontal movement
        if enemy.left < 100: 
            enemy.velocityX *= -1
            enemy.left = 100
        elif enemy.right > 300:
            enemy.velocityX *= -1
            enemy.right = 300


def bullet_movement():
    global score, bullet_list, enemy_list

    bullets_to_remove = []  # Track bullets to remove

    # Loop through each bullet
    for bullet in bullet_list:
        bullet.y = bullet.y - bullet.velocityY  # Move the bullet upward

        # If the bullet is off the screen, mark it for removal
        if bullet.y < 0:
            bullets_to_remove.append(bullet)

        for enemy in enemy_list:
            # if a bullet hits an enemy 
            if bullet.colliderect(enemy):
                # Reset enemy position
                enemy.y = 100
                enemy.x = random.randint(0, 200)

                # Mark the bullet for removal
                bullets_to_remove.append(bullet)

                break

    # Remove bullets after iteration
    for bullet in bullets_to_remove:
        bullet_list.remove(bullet)

def update():
    global game_running, score, bullet_countdown, timer

    # allow key presses at all times
    key_presses()

    # while game is running, enemies move and bullets move
    if game_running == True:
        enemy_movement()
        bullet_movement()

    # while the timer is above 0, decrease it
    if timer > 0:
        timer -= 1 / 60  # Decrease by 1/60th of a second (since update runs 60 times per second)

pgzrun.go()
