import pygame, sys, os
from pygame.locals import *

clock = pygame.time.Clock()

pygame.display.set_caption("animation testing")

WINDOW_SIZE = (1200, 800)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

display = pygame.Surface((600, 400))


global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split("/")[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + "_" + str(n)
        img_loc = path + "/" + animation_frame_id + ".png"
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    
    return action_var,frame

animation_database = {}

animation_database["walk"] = load_animation("walk",[9,9,9,9])
animation_database["idle"] = load_animation("idle",[70, 7])

moving_right = False
moving_left = False
player_action = "idle"
player_frame = 0
player_flip = False
player_movement = [50, 50]



while True:
    display.fill((34, 44, 52))
    
    
    
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
        

    if moving_right == True:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,"walk")
    elif moving_left == True:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,"walk")
    else:
        player_action,player_frame = change_action(player_action,player_frame,"idle")  
    
    

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_movement[0], player_movement[1]))
    
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True

        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False    
    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)    