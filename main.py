import pygame
from sys import exit
from random import randint, choice

from Player import Player
from Obstacle import Obstacle
            
def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True
    
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Game status
game_active = False
start_time = 0
score = 0

# Background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

title_surface = test_font.render('PixelRunner', False, (111, 196, 169))
title_rect = title_surface.get_rect(center = (400, 80))

message_surface = test_font.render('Space to play', False, (111, 196, 169))
message_rect = message_surface.get_rect(center = (400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:            
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    bg_music.play()
                    start_time = pygame.time.get_ticks()
            
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        for obstacle in obstacle_group:
            obstacle.speed += score / 100

        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collision_sprite()
        
    else:
        bg_music.stop()
        screen.fill((94, 129, 162))
        screen.blit(title_surface, title_rect)
        screen.blit(player_stand, player_stand_rect)
        
        score_message_surface = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message_surface.get_rect(center = (400, 350))
        if score == 0: screen.blit(message_surface, message_rect)
        else: screen.blit(score_message_surface, score_message_rect)
        
        player.sprite.rect.midbottom = (100, 300)
    
    pygame.display.update()
    clock.tick(60) # ceiling the framerate to 60 fps