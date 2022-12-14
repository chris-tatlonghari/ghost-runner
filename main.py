import pygame
from sys import exit
from random import randint

def display_score():
    global high_score
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = text_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    
    trophy_surface = pygame.image.load('graphics/trophy.png').convert_alpha()
    trophy_surface = pygame.transform.scale(trophy_surface, (20, 30))
    trophy_rect = trophy_surface.get_rect(center = (30, 30))
    screen.blit(trophy_surface, trophy_rect)

    high_score_surface = text_font.render(f'{high_score}', False, (230, 174, 71))
    high_score_rect = high_score_surface.get_rect(midleft = (50, 35))
    screen.blit(high_score_surface, high_score_rect)

    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                snail_animation()
                screen.blit(snail_surface, obstacle_rect)
            else:
                fly_animation()
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: 
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surface, player_index

    # Switch between walking images while player is on the floor
    if player_rect.bottom < 300:
        player_surface = player_jump
    # Display jump image while player is not on the floor
    else: 
        player_index += 0.1
        if player_index > len(player_walking): player_index = 0
        player_surface = player_walking[int(player_index)]

def snail_animation():
    global snail_surface, snail_index
    snail_index += 0.05
    if snail_index > len(snail_gliding): snail_index = 0
    snail_surface = snail_gliding[int(snail_index)]

def fly_animation():
    global fly_surface, fly_index
    fly_index += 0.1
    if fly_index > len(fly_flying): fly_index = 0
    fly_surface = fly_flying[int(fly_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400)) #(w,h)
pygame.display.set_caption('Ghost Runner')
# pygame.display.set_icon()
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
high_score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_gliding = [snail_1, snail_2]
snail_index = 0
snail_surface = snail_gliding[snail_index]
fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_flying = [fly_1, fly_2]
fly_index = 0
fly_surface = fly_flying[fly_index]

obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walking = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surface = player_walking[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = text_font.render('Ghost Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = text_font.render('Press enter to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 340))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.QUIT
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos): 
                    player_gravity = -20
            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
        else:
            if event.type== pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100), 210)))
    
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()
        

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: 
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = text_font.render(f'Your score was: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 340))
        screen.blit(game_name, game_name_rect)
        if score > high_score: high_score = score

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
