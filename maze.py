# Imports
import pygame
import intersects
import walls
import sched, time
from collections import deque

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "Literally Ian Thompson's Maze"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 48, 0)


# Make a player
player =  [15, 0, 25, 25]
player_vx = 0
player_vy = 0
player_speed = 6

# make walls
walls = walls.walls  # gets walls from the walls file

# Make coins
coin1 = [300, 500, 25, 25]
coin2 = [400, 200, 25, 25]
coin3 = [150, 150, 25, 25]
coin4 = [247, 530, 25, 25]
coin5 = [345, 246, 25, 25]
coins = [coin1, coin2, coin3, coin4, coin5]

# spawner
top_spawner = [0, -5,50,10]

spawners = [top_spawner]


# Game loop
win = False
done = False
is_game_playing = False
is_touching_spawner = False

start_ticks=pygame.time.get_ticks() #starter tick

ticks = 0

ss_options = deque([1, 0, 0])
def splash_screen():

    play_color = (255,255,255)
    high_color = (198, 198, 198)
    setting_color = (198, 198, 198)
    if ss_options[0] == 1:
        play_color = (255,255,255)
        high_color = (198, 198, 198)
        setting_color = (198, 198, 198)
    elif ss_options[1] == 1:
        play_color = (198,198,198)
        high_color = (255, 255, 255)
        setting_color = (198, 198, 198)
    elif ss_options[2] == 1:
        play_color = (198,198,198)
        high_color = (198, 198, 198)
        setting_color = (255, 255, 255)

    font = pygame.font.Font(None, 100)
    text = font.render("Ian's MAZE", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH/2, 100))
    screen.blit(text, text_rect)

    font2 = pygame.font.Font(None, 30)
    text2 = font2.render("by Ian Thompson", True, WHITE)
    text_rect2 = text2.get_rect(center=(WIDTH/2, 150))
    screen.blit(text2, text_rect2)

    font3 = pygame.font.Font(None, 50)
    text3 = font3.render("Play Now!", True, play_color)
    text_rect3 = text3.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text3, text_rect3)

    font4 = pygame.font.Font(None, 50)
    text4 = font4.render("High Scores", True, high_color)
    text_rect4 = text4.get_rect(center=(WIDTH/2, 450))
    screen.blit(text4, text_rect4)

    font5 = pygame.font.Font(None, 50)
    text5 = font5.render("Settings", True, setting_color)
    text_rect5 = text5.get_rect(center=(WIDTH/2, 550))
    screen.blit(text5, text_rect5)

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            print(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not is_game_playing:
                    is_game_playing = True
            if not is_game_playing:
                if event.key == pygame.K_UP:
                    ss_options.rotate(-1)
                if event.key == pygame.K_DOWN:
                    ss_options.rotate(1)


    pressed = pygame.key.get_pressed()

    up = pressed[pygame.K_UP] or pressed[pygame.K_w]
    down = pressed[pygame.K_DOWN] or pressed[pygame.K_s]
    left = pressed[pygame.K_LEFT] or pressed[pygame.K_a]
    right = pressed[pygame.K_RIGHT] or pressed[pygame.K_d]

    if is_game_playing:

        if not win:
            seconds=(pygame.time.get_ticks()-start_ticks)/1000
            # seconds = 0
        if up:
            player_vy = -player_speed
        elif down:
            player_vy = player_speed
        else:
            player_vy = 0

        if left:
            player_vx = -player_speed
        elif right:
            player_vx = player_speed
        else:
            player_vx = 0

        # frame = ticks // 10
        #
        # ticks += 1
        #
        # if ticks >= 60:
        #     ticks = 0
        #
        # if frame == 0:
        #     time += 1

        # Game logic (Check for collisions, update points, etc.)
        ''' move the player in horizontal direction '''
        player[0] += player_vx

        ''' resolve collisions horizontally '''
        for w in walls:
            if intersects.rect_rect(player, w):
                if player_vx > 0:
                    player[0] = w[0] - player[2]
                elif player_vx < 0:
                    player[0] = w[0] + w[2]

        ''' move the player in vertical direction '''
        player[1] += player_vy

        ''' resolve collisions vertically '''
        for w in walls:
            if intersects.rect_rect(player, w):
                if player_vy > 0:
                    player[1] = w[1] - player[3]
                if player_vy < 0:
                    player[1] = w[1] + w[3]
        for s in spawners:
            if intersects.rect_rect(player, s):
                is_touching_spawner = True


        ''' here is where you should resolve player collisions with screen edges '''
        top = player[1]
        bottom = player[1] + player[3]
        left = player[0]
        right = player[0] + player[2]


        ''' if the block is moved out of the window, nudge it back on. '''


        if top < 0:
            player[1] = 0
        elif bottom > HEIGHT:
            player[1] = HEIGHT - player[3]

        if left < 0:
            player[0] = 0
        elif right > WIDTH:
            player[0] = WIDTH - player[2]

        ''' get the coins '''
        coins = [c for c in coins if not intersects.rect_rect(player, c)]

        if len(coins) == 0:
            win = True


        # Drawing code (Describe the picture. It isn't actually drawn yet.)
        screen.fill(BLACK)

        pygame.draw.rect(screen, WHITE, player)

        for s in spawners:
            pygame.draw.rect(screen, WHITE, s)

        for w in walls:
            pygame.draw.rect(screen, RED, w)

        for c in coins:
            pygame.draw.rect(screen, YELLOW, c)

        if win:
            font = pygame.font.Font(None, 48)
            text = font.render("You Win!", 1, YELLOW)
            screen.blit(text, [400, 200])


        # pygame.draw.rect(screen, WHITE, [830,0,WIDTH - 830, 100])
        # font = pygame.font.Font(None, 50)
        # text = font.render(str(seconds), 1, BLACK)
        # screen.blit(text, [910, 10])
    else:

        splash_screen()

        # if down:
        #     print('sdf')

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
