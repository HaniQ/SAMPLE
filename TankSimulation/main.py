''''
Author: Ekram
08.02.17
Simulation for navigation of the buggy
TODO: Current field scanned % is not correct. Think of new one
'''

import pygame
from pygame.locals import *
from utilities import *
from Background import *
from Tank import *


def main():

#Initialize Everything
    screen_width = 1500
    screen_height = 800
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Navigation Simulation')

#Sprite background
    bg = Background(0,0, 'b1.jpg')

#Set game FPS
    FPS = 30

#Prepare Game Objects
    clock = pygame.time.Clock()

#field
    Field_x1 = 700
    Field_x2 = 1300
    Field_y1 = 120
    Field_y2 = 720
    Buggy_Dimensions = 50
    wall_sprite_group = pygame.sprite.Group()
    z = Field_x2-Field_x1
    w = Field_y2-Field_y1
    my_wall1 = Collision_Line(Field_x1,Field_y1,z,w)
    wall_sprite_group.add(my_wall1)

    Number_of_grids = round(((Field_x2-Field_x1)*(Field_y2-Field_y1))/(Buggy_Dimensions*Buggy_Dimensions))
    percentage_per_grid = round((1/Number_of_grids)*100,4)


#text
    
    # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
    myfont = pygame.font.SysFont("monospace", 35)

    # render text
    label1 = myfont.render("Percentage of Field scanned: ", 1, (255,255,255))

    label2 = myfont.render("Number of Grids: ", 1, (255,255,255))
    label2_answer = myfont.render(str(Number_of_grids), 1, (255,255,255))  
      
    label3 = myfont.render("Each grid in % is apprx: ", 1, (255,255,255))
    label3_answer = myfont.render(str(percentage_per_grid), 1, (255,255,255))

#player declarations
    tank = Tank(400,400, Field_x1, Field_x2, Field_y1, Field_y2, Buggy_Dimensions) 


#Adding to super group which will handle drawing

    allsprites = pygame.sprite.LayeredUpdates((bg, wall_sprite_group, tank))

    
#Main Loop
    going = True
    
    #bgm.play()
    while going:

        clock.tick(FPS)

        field_scanned_percentage = tank.Fetch_Field_Percentage_Scanned()
        if field_scanned_percentage!='##':
            if field_scanned_percentage>100:
                field_scanned_percentage=100
        label1_answer = myfont.render(str(field_scanned_percentage), 1, (255,255,255))

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False 

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False

            elif event.type == KEYDOWN and event.key == K_q:
                tank.Current_X_position = 400
                tank.Current_Y_position = 400
                tank.Update_Field_Coordinates(Field_x1, Field_y1, Field_x2, Field_y2)
                tank.Navigate_Bool = False
                tank.Field_Scanned_Perc = 0
                tank.Update_Animation('Reset')

            elif event.type == KEYDOWN and event.key == K_DOWN:
                tank.Update_Animation('Move_Down')

            elif event.type == KEYUP and event.key == K_DOWN:
                tank.Update_Animation('Idle')

            elif event.type == KEYDOWN and event.key == K_UP:
                tank.Update_Animation('Move_Up')

            elif event.type == KEYUP and event.key == K_UP:
                tank.Update_Animation('Idle')

            elif event.type == KEYDOWN and event.key == K_LEFT:
                tank.Update_Animation('Move_Left')

            elif event.type == KEYUP and event.key == K_LEFT:
               tank.Update_Animation('Idle')

            elif event.type == KEYDOWN and event.key == K_RIGHT:
                tank.Update_Animation('Move_Right')

            elif event.type == KEYUP and event.key == K_RIGHT:
                tank.Update_Animation('Idle')

            elif event.type == KEYDOWN and event.key == K_p:
                tank.Current_X_position = Field_x1
                tank.Current_Y_position = Field_y1
                tank.Update_Animation('Navigate_Right')

            elif event.type == KEYDOWN and event.key == K_w:
                tank.Print_Ending_Array()

        allsprites.update()
 

        #Draw Everything

        allsprites.draw(screen)       
        screen.blit(label1, (15, 100))
        screen.blit(label1_answer, (600, 100))

        screen.blit(label2, (15, 200))
        screen.blit(label2_answer, (420, 200))

        screen.blit(label3, (15, 300))
        screen.blit(label3_answer, (520, 300))


        pygame.display.flip()

    pygame.quit()




if __name__ == '__main__':
    main()
