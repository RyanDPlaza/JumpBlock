import sys

import pygame
import pickle
import os

pygame.init()

# main window
WIDTH = 960
HEIGHT = 540
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

# default variables
block_num = 0

class Block():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 100, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)


class spike():
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = 30
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((150, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)


class EmptyBlock():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)



def mouse_pos():
    return pygame.mouse.get_pos()


while True:
    pressed_keys = pygame.key.get_pressed()
    # event checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # changing block to be placed
        if pressed_keys[pygame.K_b]:
            block_num = 1
        if pressed_keys[pygame.K_s]:
            block_num = 2
        if pressed_keys[pygame.K_BACKSPACE]:
            block_num = 0

        if event.type == pygame.MOUSEBUTTONDOWN:  # checking if mouse button was pressed
            for obj in obj_list:  # iterating through all objects on map
                if obj.rect.left < mouse_pos()[0] < obj.rect.right \
                        and obj.rect.top < mouse_pos()[1] < obj.rect.bottom:  # if mouse pos was in an obj when pressed
                    x_index = int(obj.rect.x / 30)
                    y_index = int(obj.rect.y / 30)
                    world.world_data[y_index][x_index] = self.block_num
            world.draw()  # only redraws / updates world if something changed

    # drawing
    screen.fill(WHITE)

    # displaying map
    for obj in obj_list:
        screen.blit(obj.surf, obj.rect)
        pygame.draw.rect(screen, (0, 0, 0), obj.rect, 1)

    # updating the display
    screen.blit(update_fps(), (10, 0))
    pygame.display.update()
