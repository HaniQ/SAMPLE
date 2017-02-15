''''
Author: Ekram
08.02.17
Simulation for navigation of the buggy
As of now buggy is modelled as a particle with all collisions as 100% elastic
No force, weight, inertia, momentum yet  <---- work on these when free
Need to work on modelling the physical buggy as well/ right now its just a rectangle box
Meant to also be used to test genetic evolution and machine learning algorithms as side project

'''

import pygame
from pygame.locals import *
from utilities import *
from Background import *
from Tank import *
from Grass import *


def main():

    Green = (34,139,34)
    White = (255,255,255)
    Blue = (0,0,255)

#Initialize Everything
    screen_width = 1500
    screen_height = 800
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Navigation Simulation')

#Sprite background
    bg = Background(0,0, 'b1.jpg')
    grass = Grass(700,120, 'grass.jpg')

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
    field_sprite_group = pygame.sprite.LayeredUpdates()
    z = Field_x2-Field_x1
    w = Field_y2-Field_y1
    Field = Collision_Line(Field_x1,Field_y1,z,w, Green)
    field_sprite_group.add(Field)

    Number_of_grids = round(((Field_x2-Field_x1)*(Field_y2-Field_y1))/(Buggy_Dimensions*Buggy_Dimensions))
    percentage_per_grid = round((1/Number_of_grids)*100,4)

#Field Boundary lines
    wall_sprite_group_horz_bottom = pygame.sprite.LayeredUpdates()
    wall_sprite_group_horz_top = pygame.sprite.LayeredUpdates()
    wall_sprite_group_vert_right = pygame.sprite.LayeredUpdates()
    wall_sprite_group_vert_left = pygame.sprite.LayeredUpdates()

    Bound_Line1 = Collision_Line(Field_x1,Field_y1,z,3, White)
    Inner_Bound_Line1 = Collision_Line(900,320,500,3, White)
    wall_sprite_group_horz_top.add(Bound_Line1)
    

    Bound_Line2 = Collision_Line(Field_x1,Field_y2,z,3, White)
    Inner_Bound_Line2 = Collision_Line(900,310,500,3, White)
    Inner_Bound_Line3 = Collision_Line(400,517,700,3, White)
    wall_sprite_group_horz_bottom.add(Bound_Line2)
    

    Bound_Line3 = Collision_Line(Field_x1,Field_y1,3,w, White)
    Inner_Bound_Line4 = Collision_Line(1100,517,3,400, White)
    wall_sprite_group_vert_left.add(Bound_Line3)

    Bound_Line4 = Collision_Line(Field_x2,Field_y1,3,w, White)
    wall_sprite_group_vert_right.add(Bound_Line4)

#Field covering squares
    Field_Scanned_Squares_Group = pygame.sprite.LayeredUpdates()

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
    allsprites = pygame.sprite.LayeredUpdates((bg, field_sprite_group,grass, wall_sprite_group_horz_bottom, wall_sprite_group_horz_top, wall_sprite_group_vert_left, wall_sprite_group_vert_right, Field_Scanned_Squares_Group, tank))

    
#Main Loop
    going = True
    Square_Paint_Bool = False
    
    #bgm.play()
    while going:

        clock.tick(FPS)

        '''square place on field for scanned stuff'''
        if tank.Place_Square_Bool==True and Square_Paint_Bool==True:
            Square = Collision_Line(tank.Square_X,tank.Square_Y,50,50, Blue)
            Field_Scanned_Squares_Group.add(Square)
            allsprites.add(Square)
            tank.Place_Square_Bool=False

        '''field scanned stuff'''
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
                '''removing all the blue squares: get the list and then iterate over them removing each from allsprites'''
                Square_To_Remove_List = Field_Scanned_Squares_Group.sprites()
                for shape in Square_To_Remove_List:
                    allsprites.remove(shape)

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

            elif event.type == KEYDOWN and event.key == K_m:
                tank.Current_X_position = Field_x1+50
                tank.Current_Y_position = Field_y1+50
                tank.Update_Animation('Machine_Learning_Start')

            elif event.type == KEYDOWN and event.key == K_w:
                tank.Print_Ending_Array()

            elif event.type == KEYDOWN and event.key == K_z:
                tank.Update_Animation('Diagonal')

            elif event.type == KEYDOWN and event.key == K_a:
                wall_sprite_group_horz_top.add(Inner_Bound_Line1)
                wall_sprite_group_horz_bottom.add(Inner_Bound_Line2)
                wall_sprite_group_horz_bottom.add(Inner_Bound_Line3)
                wall_sprite_group_vert_left.add(Inner_Bound_Line4)

                allsprites.remove(wall_sprite_group_horz_bottom)
                allsprites.remove(wall_sprite_group_horz_top)

                allsprites.remove(wall_sprite_group_vert_left)

                allsprites.add(wall_sprite_group_horz_bottom)
                allsprites.add(wall_sprite_group_horz_top)

                allsprites.add(wall_sprite_group_vert_left)

            elif event.type == KEYDOWN and event.key == K_s:
                allsprites.remove(Inner_Bound_Line1)
                allsprites.remove(Inner_Bound_Line2)
                allsprites.remove(Inner_Bound_Line3)
                allsprites.remove(Inner_Bound_Line4)

                wall_sprite_group_horz_top.remove(Inner_Bound_Line1)
                wall_sprite_group_horz_bottom.remove(Inner_Bound_Line2)
                wall_sprite_group_horz_bottom.remove(Inner_Bound_Line3)
                wall_sprite_group_vert_left.remove(Inner_Bound_Line4)

                allsprites.remove(wall_sprite_group_horz_bottom)
                allsprites.remove(wall_sprite_group_horz_top)
                allsprites.remove(wall_sprite_group_vert_left)

                allsprites.add(wall_sprite_group_horz_bottom)
                allsprites.add(wall_sprite_group_horz_top)
                allsprites.add(wall_sprite_group_vert_left)

            elif event.type == KEYDOWN and event.key == K_r:
                Square_Paint_Bool=True

            elif event.type == KEYDOWN and event.key == K_t:
                Square_Paint_Bool=False


        allsprites.remove(tank)
        tank.update(wall_sprite_group_horz_bottom, wall_sprite_group_horz_top, wall_sprite_group_vert_left, wall_sprite_group_vert_right)
        allsprites.update()
        allsprites.add(tank)
        allsprites.move_to_back(bg)
 
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
