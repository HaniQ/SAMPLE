
'''
Background sprite and collision wall
'''

import pygame
from utilities import *




class Background(pygame.sprite.Sprite):
    '''generates the background and contains logic to make it scroll'''

    def __init__(self, Start_X, Start_Y, background_name):

        self.background_name = background_name

        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        self.image, self.rect = load_image(self.background_name, 'Background')

        self.Current_X_position = Start_X
        self.Current_Y_position = Start_Y

        self.rect.topleft = self.Current_X_position, self.Current_Y_position

        self.Current_Animation = 'Idle'

        self.Map_Movement_Factor = 12

    def update(self):

        if self.Current_Animation=='Idle':
            '''do nothing'''
            return None





class Collision_Line(pygame.sprite.Sprite):

    def __init__(self, Start_X, Start_Y, width, height):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        self.image = pygame.Surface([width,height])
        self.image.fill((34,139,34))

        self.rect = self.image.get_rect()
        self.rect.y = Start_Y
        self.rect.x = Start_X

