'''
couple of helper functions
'''

import os, pygame
from pygame.compat import geterror


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def load_image(name, folderName):
    fullnamewithFoldername = os.path.join(data_dir, folderName)
    fullname = os.path.join(fullnamewithFoldername, name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()

    return image, image.get_rect()

def load_sound(name, folderName):

    fullnamewithFoldername = os.path.join(data_dir, folderName)
    print (fullnamewithFoldername)
    fullname = os.path.join(fullnamewithFoldername, name)
    print (fullname)

    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(fullnamewithFoldername, name)
    try:
        sound = pygame.mixer.Sound(fullname)
        sound.set_volume(0.5)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


def load_sprite_image(name, f1, f2, f3, f4):
    fullnamewithFoldername = os.path.join(data_dir, f1, f2, f3, f4)
    fullname = os.path.join(fullnamewithFoldername, name)

    try:
        image = pygame.image.load(fullname)
        #image.set_colorkey((0,0,0))
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    #image = image.convert()

    return image, image.get_rect()


def load_skill_image(name, ClassName, SkillName):
    fullnamewithFoldername = os.path.join(data_dir, ClassName, SkillName)
    fullname = os.path.join(fullnamewithFoldername, name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    #image = image.convert()

    return image, image.get_rect()

