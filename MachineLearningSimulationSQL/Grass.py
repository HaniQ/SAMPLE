

import pygame
from utilities import *




class Grass(pygame.sprite.Sprite):
    '''generates the background and contains logic to make it scroll'''

    def __init__(self, Start_X, Start_Y, background_name):

        self.background_name = background_name

        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        self.image, self.rect = load_image(self.background_name, 'Background')

        self.Current_X_position = Start_X
        self.Current_Y_position = Start_Y

        self.rect.topleft = self.Current_X_position, self.Current_Y_position

        self.Current_Animation = 'Idle'


    def update(self):

        if self.Current_Animation=='Idle':
            '''do nothing'''
            return None