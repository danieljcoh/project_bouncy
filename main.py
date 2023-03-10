import pygame
from sys import exit
from random import randint

# TIMESTAMP: 2:37:00

# Todo
# 1. Change Icon


# FUNCTIONS
def display_score():
    # gives the time in milliseconds
    current_time = round(pygame.time.get_ticks() / 1000) - round(start_time / 1000)
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_surf_shadow = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rectangle = score_surf.get_rect(left=2, top=2)

    screen.blit(score_surf, score_rectangle)
    screen.blit(score_surf_shadow, score_rectangle)

    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            screen.blit(snail_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > 0]

        return obstacle_list

    else:
        return []


# Calling Pygame first to access pygame functionality that otherwise wouldn't be accessible
pygame.init()

# A display surface (screen): The window a player sees -- Has to be created
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Project Bouncy House")

# Change ICON
clock = pygame.time.Clock()

# create a font in pygame Font(font type, font size) Pygame default font: None
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# GAME STATE
game_active = False
start_time = 0
score = 0

# SURFACES #
sky_surface = pygame.image.load('graphics/Sky.png').convert()  # convert allows pygame an easier time with the images
ground_surface = pygame.image.load('graphics/ground.png').convert()

# render(text, AA=Smooth the edges of the text, color)
text_surface = test_font.render('Project Bouncy', False, (64, 64, 64))
text_surface_shadow = test_font.render('Project Bouncy', False, 'azure4')

# End Screen text
text_surface_title = test_font.render('Project Bouncy', False, (255, 255, 255))
text_surface_title_shdw = test_font.render('Project Bouncy', False, (0, 0, 0))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Snail / OBSTACLE Information #
snail_surface = pygame.image.load('graphics/snail1.png').convert_alpha()  # convert alpha gets rid of white boxes around
snail_rectangle = snail_surface.get_rect(left=600, top=250)

obstacle_rect_list = []

# Player Information #
player_surface = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
# Rect(left,top,width,height)
# .get_rect(player_surface) and draws a rectangle around the surface
player_rectangle = player_surface.get_rect(left=80, top=202)  # 57m in video
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load("graphics/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # MOUSE COLLISION
            if event.type == pygame.MOUSEBUTTONDOWN:  # gets if the mouse is moved and can print a pos
                if player_rectangle.collidepoint(event.pos):
                    if player_rectangle.bottom == 290 and player_rectangle.bottom == 290:
                        player_gravity = -20
            # SPACE BAR
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom == 290:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rectangle.left = 800
                start_time = pygame.time.get_ticks()

        if event.type == obstacle_timer and game_active:
            obstacle_rect_list.append(snail_surface.get_rect(left=randint(900, 1100), top=250))

    if game_active:
        # blit(surface, position) = block image transfer
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 283))
        screen.blit(text_surface_shadow, (287, 51))
        screen.blit(text_surface, (285, 50))
        score = display_score()

        # draw the rect twice to get a margin around the text
        # #pygame.draw.rect(screen, '#c0e8ec', score_rectangle)
        # #pygame.draw.rect(screen, '#c0e8ec', score_rectangle, 10)

        # draw a line as practice
        # pygame.draw.line(screen, "Red", (0, 0), pygame.mouse.get_pos(), 10)

        # to move the snail to the left using the rectangle
        # otherwise it would just be the x-axis variable

        ### snail_rectangle.left -= 5
        ### if snail_rectangle.right <= 0:
        ###     snail_rectangle.left = 850
        ### screen.blit(snail_surface, snail_rectangle)

        # player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom > 290:
            player_rectangle.bottom = 290
        screen.blit(player_surface, player_rectangle)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        if snail_rectangle.colliderect(player_rectangle):
            game_active = False
    else:  # if the game is lost or intro or menu screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f"Score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(text_surface_title_shdw, (290, 53))
            screen.blit(text_surface_title, (287, 51))
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()  # updates the display surface
    clock.tick(60)  # this tells the while loop to run faster than 60FPS

