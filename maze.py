# maze.py
#
# By Ian Thompson
# Computer Programming

# Imports
import pygame
import intersects
import walls
from collections import deque
import get_high_scores



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
GREEN = (0, 255, 0)

player_vx = 0
player_vy = 0
player_speed = 20

player2_vx = 0
player2_vy = 0
player2_speed = 20

wall = walls.walls


def setup():
    global player2, coins_collected2, time_remaining, player, coins, switch, doors, win, collidables, done, is_game_playing, should_show_splash, is_touching_spawner,show_high_score_screen, coins_collected, ticks, start_ticks, doors_open, walls
    # Make a player
    player =  [8, 8, 25, 25]
    player2 =  [975, 674, 25, 25]


    # make walls
    # walls = walls.walls


    for w in wall:
        walls = wall

    # Make coins
    coin1 = [20, 150, 25, 25]
    coin2 = [400, 180, 25, 25]
    coin3 = [150, 150, 25, 25]
    coin4 = [247, 530, 25, 25]
    coin5 = [345, 246, 25, 25]
    coin6 = [350, 387, 25, 25]
    coin7 = [172, 395, 25, 25]
    coin8 = [164, 524, 25, 25]
    coin9 = [164, 524, 25, 25]
    coin10 = [447, 513, 25, 25]
    #coins = [coin1, coin2, coin3, coin4, coin5, coin6,
     #        coin7, coin8, coin9, coin10]

    coins = [coin1, coin2]

    switch = [185, 670, 25, 25]
    door1 = [378, 418, 50, 25]


    doors = [door1]

    collidables = walls + doors

    # Game loop and Booleans
    win = False
    done = False
    is_game_playing = False
    should_show_splash = True
    is_touching_spawner = False
    show_high_score_screen = False
    coins_collected = 0
    coins_collected2 = 0
    doors_open = False
    
    time_remaining = -1
    

    start_ticks = 0 #starter tick

    ticks = 0

setup()

def end_screen():

    if coins_collected > coins_collected2:
        win =  "Player 1 Wins!"
    else:
        win = "Player 2 Wins!"

    screen.fill(BLACK)
    font = pygame.font.Font(None, 100)
    text = font.render(win, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH/2, 100))
    screen.blit(text, text_rect)

    font2 = pygame.font.Font(None, 100)
    text2 = font2.render('You collected ' + str(coins_collected) + ' coins', True, WHITE)
    text_rect2 = text2.get_rect(center=(WIDTH/2, 200))
    screen.blit(text2, text_rect2)
    


while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            print(event.pos)  # prints where mouse click event occured
        if event.type == pygame.KEYDOWN:
            if win:
                if event.key == pygame.K_SPACE:
                    setup()

    pressed = pygame.key.get_pressed()

    up = pressed[pygame.K_UP]
    down = pressed[pygame.K_DOWN]
    left = pressed[pygame.K_LEFT]
    right = pressed[pygame.K_RIGHT]

    w_up = pressed[pygame.K_w]
    a_down = pressed[pygame.K_s]
    s_left = pressed[pygame.K_a]
    d_right = pressed[pygame.K_d]


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


    if w_up:
        player2_vy = -player2_speed
    elif a_down:
        player2_vy = player2_speed
    else:
        player2_vy = 0

    if s_left:
        player2_vx = -player2_speed
    elif d_right:
        player2_vx = player2_speed
    else:
        player2_vx = 0


    # Game logic (Check for collisions, update points, etc.)
    ''' move the player in horizontal direction '''
    player[0] += player_vx
    player2[0] += player2_vx


    ''' resolve collisions horizontally '''
    for c in collidables:
        if intersects.rect_rect(player, c):
            if player_vx > 0:
                player[0] = c[0] - player[2]
            elif player_vx < 0:
                player[0] = c[0] + c[2]
        if intersects.rect_rect(player2, c):
            if player2_vx > 0:
                player2[0] = c[0] - player2[2]
            elif player2_vx < 0:
                player2[0] = c[0] + c[2]

    ''' move the player in vertical direction '''
    player[1] += player_vy
    player2[1] += player2_vy

    ''' resolve collisions vertically '''
    for c in collidables:
        if intersects.rect_rect(player, c):
            if player_vy > 0:
                player[1] = c[1] - player[3]
            if player_vy < 0:
                player[1] = c[1] + c[3]
        if intersects.rect_rect(player2, c):
            if player2_vy > 0:
                player2[1] = c[1] - player2[3]
            if player2_vy < 0:
                player2[1] = c[1] + c[3]

    ''' here is where you should resolve player collisions with screen edges '''
    top = player[1]
    bottom = player[1] + player[3]
    left = player[0]
    right = player[0] + player[2]

    top2 = player2[1]
    bottom2 = player2[1] + player2[3]
    left2 = player2[0]
    right2 = player2[0] + player2[2]

    ''' if the block is moved out of the window, nudge it back on. '''


    if top < 0:
        player[1] = 0
    elif bottom > HEIGHT:
        player[1] = HEIGHT - player[3]

    if left < 0:
        player[0] = 0
    elif right > WIDTH:
        player[0] = WIDTH - player[2]

    if top2 < 0:
        player2[1] = 0
    elif bottom2 > HEIGHT:
        player2[1] = HEIGHT - player2[3]

    if left2 < 0:
        player2[0] = 0
    elif right2 > WIDTH:
        player2[0] = WIDTH - player2[2]

    ''' get the coins '''
    hit_list = [c for c in coins if intersects.rect_rect(player, c)]
    hit_list2 = [c for c in coins if intersects.rect_rect(player2, c)]

    for hit in hit_list:
        coins.remove(hit)
        coins_collected += 1
        print("sound!")

    for hit in hit_list2:
        coins.remove(hit)
        coins_collected2 += 1
        print("sound!")

    if len(coins) == 0:
        win = True

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, player2)


    for w in walls:
        pygame.draw.rect(screen, RED, w)

    for c in coins:
        pygame.draw.rect(screen, YELLOW, c)

    if not doors_open:
        for d in doors:
            pygame.draw.rect(screen, RED, d)

    if intersects.rect_rect(player, switch):
        doors_open = True

        collidables = [c for c in collidables if c not in doors]

    if intersects.rect_rect(player2, switch):
        doors_open = True

        collidables = [c for c in collidables if c not in doors]

    # Draw Switches
    pygame.draw.rect(screen, GREEN, [185, 670, 25, 25])

    if win:
        end_screen()

    if not win:
        ticks += 1

        if ticks % 60 == 0:
            time_remaining -= 1
        if time_remaining == 0:
            win = True

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()

# Initialize game engine
# pygame.init()
#
#
# # Window
# WIDTH = 1000
# HEIGHT = 700
# SIZE = (WIDTH, HEIGHT)
# TITLE = "Literally Ian Thompson's Maze"
# screen = pygame.display.set_mode(SIZE)
# pygame.display.set_caption(TITLE)
#
#
#
#
# # Timer
# clock = pygame.time.Clock()
# refresh_rate = 60
#
# # Colors
# RED = (255, 0, 0)
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# YELLOW = (255, 255, 0)
# GREEN = (0, 255, 0)
#
#
# # Make a player
# player =  [15, 0, 25, 25]
# player_vx = 0
# player_vy = 0
# player_speed = 6
#
# # make walls
# walls = walls.walls  # gets walls from the walls file
#
# switch = [185, 670, 25, 25]
# door1 = [378, 418, 50, 25]
#
#
# doors = [door1]
#
# collidables = walls + doors
#
# # Make coins
# coin1 = [20, 150, 25, 25]
# coin2 = [400, 180, 25, 25]
# coin3 = [150, 150, 25, 25]
# coin4 = [247, 530, 25, 25]
# coin5 = [345, 246, 25, 25]
# coin6 = [350, 387, 25, 25]
# coin7 = [172, 395, 25, 25]
# coin8 = [164, 524, 25, 25]
# coin9 = [164, 524, 25, 25]
# coin10 = [447, 513, 25, 25]
# #coins = [coin1, coin2, coin3, coin4, coin5, coin6,
#  #        coin7, coin8, coin9, coin10]
#
# coins = [coin1, coin2]
#
# # spawner
# top_spawner = [0, -5, 50, 10]
#
# spawners = [top_spawner]
#
#
# # Game loop and Booleans
# win = False
# done = False
# is_game_playing = False
# should_show_splash = True
# is_touching_spawner = False
# show_high_score_screen = False
# coins_collected = 0
# doors_open = False
#
#
# start_ticks = 0 #starter tick
#
# ticks = 0
# def calculate_score(time, coins):
#     global multiplier
#     multiplier = 1
#
#     # The multiplier variable is set to one at default. The code below will calculate
#     # the correct score bassed on the time it took to complete the maze.
#     # After the multiplier value has been determined, the number of coins collected, times the multiplier,
#     # plus 100 is returned as the final score.
#
#     if time >= 60:
#         multiplier = 1
#     if time <= 50 and time >= 40:
#         multiplier = 0.5
#     if time <= 49 and time >= 30:
#         multiplier = 2
#     if time <= 29 and time >= 15:
#         multiplier = 3
#     if time < 15:
#         multiplier = 5
#
#     return (coins_collected * multiplier) + 100  # Returns the calculated score
#
# ss_options = deque([1, 0, 0])
# # List which keeps track of which menu item is selected. If the value is one,
# # then that item is active. Each element corresponds with the position as seen on screen.
# def splash_screen():
#     screen.fill(BLACK)
#
#     play_color = (255,255,255)
#     high_color = (198, 198, 198)
#     setting_color = (198, 198, 198)
#
#     # The code below will check the status of the 'ss_options' list and set
#     # the font colors of each selection accordingly.
#     if ss_options[0] == 1:  # PLAY is the current selection
#         play_color = (255,255,255)
#         high_color = (198, 198, 198)
#         setting_color = (198, 198, 198)
#     elif ss_options[1] == 1:  # HIGH SCORE is the current selection
#         play_color = (198,198,198)
#         high_color = (255, 255, 255)
#         setting_color = (198, 198, 198)
#     elif ss_options[2] == 1:  # SETTINGS is the current selection
#         play_color = (198,198,198)
#         high_color = (198, 198, 198)
#         setting_color = (255, 255, 255)
#
#     font = pygame.font.Font(None, 100)
#     text = font.render("Ian's MAZE", True, WHITE)
#     text_rect = text.get_rect(center=(WIDTH/2, 100))
#     screen.blit(text, text_rect)
#
#     font2 = pygame.font.Font(None, 30)
#     text2 = font2.render("by Ian Thompson", True, WHITE)
#     text_rect2 = text2.get_rect(center=(WIDTH/2, 150))
#     screen.blit(text2, text_rect2)
#
#     font3 = pygame.font.Font(None, 50)
#     text3 = font3.render("Play Now!", True, play_color)
#     text_rect3 = text3.get_rect(center=(WIDTH/2, HEIGHT/2))
#     screen.blit(text3, text_rect3)
#
#     font4 = pygame.font.Font(None, 50)
#     text4 = font4.render("High Scores", True, high_color)
#     text_rect4 = text4.get_rect(center=(WIDTH/2, 450))
#     screen.blit(text4, text_rect4)
#
#     font5 = pygame.font.Font(None, 50)
#     text5 = font5.render("Settings", True, setting_color)
#     text_rect5 = text5.get_rect(center=(WIDTH/2, 550))
#     screen.blit(text5, text_rect5)
#
#
# def high_score_screen():
#     screen.fill(BLACK)
#
#     with open('high_scores.txt', 'r') as f:
#         words = f.read().splitlines()
#         first = words[0]
#         second = words[1]
#         third = words[2]
#
#     font = pygame.font.Font(None, 100)
#     text = font.render('High Scores', True, WHITE)
#     text_rect = text.get_rect(center=(WIDTH/2, 100))
#     screen.blit(text, text_rect)
#
#     font2 = pygame.font.Font(None, 50)
#     text2 = font2.render(first, True, WHITE)
#     text_rect2 = text2.get_rect(center=(WIDTH/2, 250))
#     screen.blit(text2, text_rect2)
#
#     font3 = pygame.font.Font(None, 50)
#     text3 = font3.render(second, True, WHITE)
#     text_rect3 = text3.get_rect(center=(WIDTH/2, 350))
#     screen.blit(text3, text_rect3)
#
#     font4 = pygame.font.Font(None, 50)
#     text4 = font4.render(third, True, WHITE)
#     text_rect4 = text4.get_rect(center=(WIDTH/2, 450))
#     screen.blit(text4, text_rect4)
#
# def win_screen(time, coins):
#
#     high_scores = get_high_scores.scores
#     screen.fill(BLACK)
#
#     score = calculate_score(time, coins)
#
#     font = pygame.font.Font(None, 100)
#     text = font.render('You Win!', True, WHITE)
#     text_rect = text.get_rect(center=(WIDTH/2, 100))
#     screen.blit(text, text_rect)
#
#     font2 = pygame.font.Font(None, 50)
#     text2 = font2.render('You finished in..... ' + str(int(time)) + ' seconds', True, WHITE)
#     text_rect2 = text2.get_rect(center=(WIDTH/2, 200))
#     screen.blit(text2, text_rect2)
#
#     font3 = pygame.font.Font(None, 50)
#     text3 = font3.render('You collected...... ' + str(coins) + ' coins', True, WHITE)
#     text_rect3 = text3.get_rect(center=(WIDTH/2, 300))
#     screen.blit(text3, text_rect3)
#
#     font4 = pygame.font.Font(None, 85)
#     text4 = font4.render('Total: ' + str(score) + ' points', True, WHITE)
#     text_rect4 = text4.get_rect(center=(WIDTH/2, 450))
#     screen.blit(text4, text_rect4)
#
# def restart():
#     global win, done, is_game_playing,should_show_splash, is_touching_spawner, show_high_score_screen, coins_collected, doors_open
#     win = False
#     done = False
#     is_game_playing = False
#     should_show_splash = True
#     is_touching_spawner = False
#     show_high_score_screen = False
#     coins_collected = 0
#     doors_open = False
#
#
#
#     #
#
# while not done:
#
#     # Event processing (React to key presses, mouse clicks, etc.)
#     ''' for now, we'll just check to see if the X is clicked '''
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#         if event.type == pygame.MOUSEBUTTONUP:
#             print(event.pos)  # prints where mouse click event occured
#             print(should_show_splash)
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RETURN:
#                 if not is_game_playing and ss_options[0] == 1:  # enter is pressed and PLAY is the current selection
#                     is_game_playing = True
#                     start_ticks=pygame.time.get_ticks()
#
#                 if not is_game_playing and ss_options[1] == 1:
#                     should_show_splash = False
#                     show_high_score_screen = True
#             if not is_game_playing:
#                 if event.key == pygame.K_UP:
#                     ss_options.rotate(-1)  # shifts elements in list back one
#                 if event.key == pygame.K_DOWN:
#                     ss_options.rotate(1)  # shifts elements in list foward one
#             if event.key == pygame.K_ESCAPE:
#                 if show_high_score_screen:
#                     show_high_score_screen = False
#                     should_show_splash = True
#             if event.key == pygame.K_SPACE:
#                 if win:
#                     restart()
#
#     pressed = pygame.key.get_pressed()
#
#     up = pressed[pygame.K_UP] or pressed[pygame.K_w]
#     down = pressed[pygame.K_DOWN] or pressed[pygame.K_s]
#     left = pressed[pygame.K_LEFT] or pressed[pygame.K_a]
#     right = pressed[pygame.K_RIGHT] or pressed[pygame.K_d]
#
#     if win:  # the player has either completed the maze, and or collected all the coins.
#         win_screen(seconds, coins_collected)  # Displays the win screen containing releveant information
#     elif is_game_playing:
#         should_show_splash = False
#         seconds=(pygame.time.get_ticks()-start_ticks)/1000
#             # seconds = 0
#         if up:
#             player_vy = -player_speed
#         elif down:
#             player_vy = player_speed
#         else:
#             player_vy = 0
#
#         if left:
#             player_vx = -player_speed
#         elif right:
#             player_vx = player_speed
#         else:
#             player_vx = 0
#
#         # Game logic (Check for collisions, update points, etc.)
#         ''' move the player in horizontal direction '''
#         player[0] += player_vx
#
#         ''' resolve collisions horizontally '''
#         for c in collidables:
#             if intersects.rect_rect(player, c):
#                 if player_vx > 0:
#                     player[0] = c[0] - player[2]
#                 elif player_vx < 0:
#                     player[0] = c[0] + c[2]
#
#         ''' move the player in vertical direction '''
#         player[1] += player_vy
#
#         ''' resolve collisions vertically '''
#         for c in collidables:
#             if intersects.rect_rect(player, c):
#                 if player_vy > 0:
#                     player[1] = c[1] - player[3]
#                 if player_vy < 0:
#                     player[1] = c[1] + c[3]
#
#
#         ''' here is where you should resolve player collisions with screen edges '''
#         top = player[1]
#         bottom = player[1] + player[3]
#         left = player[0]
#         right = player[0] + player[2]
#
#
#         ''' if the block is moved out of the window, nudge it back on. '''
#
#
#         if top < 0:
#             player[1] = 0
#         elif bottom > HEIGHT:
#             player[1] = HEIGHT - player[3]
#
#         if left < 0:
#             player[0] = 0
#         elif right > WIDTH:
#             player[0] = WIDTH - player[2]
#
#         ''' get the coins '''
#         hit_list = [c for c in coins if intersects.rect_rect(player, c)]
#
#         for hit in hit_list:
#             coins.remove(hit)
#             coins_collected += 1
#             print("sound!")
#
#         if len(coins) == 0:
#             win = True
#
#
#         # Drawing code (Describe the picture. It isn't actually drawn yet.)
#         screen.fill(BLACK)
#
#         pygame.draw.rect(screen, WHITE, player)
#
#         for s in spawners:
#             pygame.draw.rect(screen, WHITE, s)
#
#         for w in walls:
#             pygame.draw.rect(screen, RED, w)
#
#         for c in coins:
#             pygame.draw.rect(screen, YELLOW, c)
#
#         if not doors_open:
#             for d in doors:
#                 pygame.draw.rect(screen, RED, d)
#
#         if intersects.rect_rect(player, switch):
#             doors_open = True
#
#             collidables = [c for c in collidables if c not in doors]
#
#         # Draw Switches
#         pygame.draw.rect(screen, GREEN, [185, 670, 25, 25])
#
#     elif should_show_splash:
#         splash_screen()
#     elif show_high_score_screen:
#         high_score_screen()
#     else:
#         pass
#
#
#     # Update screen (Actually draw the picture in the window.)
#     pygame.display.flip()
#
#
#     # Limit refresh rate of game loop
#     clock.tick(refresh_rate)
#
#
# # Close window and quit
# pygame.quit()
