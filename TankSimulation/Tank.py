'''
tank sprite
will contain the logic and update statements of the tank/car sprite
'''

import pygame
from utilities import *
import random


class Tank(pygame.sprite.Sprite):
    '''generates the background and contains logic to make it scroll'''

    def __init__(self, Start_X, Start_Y, x1,x2,y1,y2, buggy_dimensions):

        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        self.image, self.rect = load_image('car.png', 'Car')
        self.image.set_colorkey((255,255,255))

        self.Current_X_position = Start_X
        self.Current_Y_position = Start_Y

        self.rect.center = self.Current_X_position, self.Current_Y_position

        self.Current_Animation = 'Idle'
        self.Navigate_Bool = False  #need dis for idle arg branch and in general a history of the last action performed was navigate

        self.Buggy_Speed = 10
        self.Buggy_Dimensions = buggy_dimensions #treat it as a square for now

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.Number_of_grids = round(((self.x2-self.x1)*(self.y2-self.y1))/(self.Buggy_Dimensions*self.Buggy_Dimensions))
        self.percentage_per_grid = round((1/self.Number_of_grids)*100,4)

        self.Field_Scanned_Perc = 0

        self.ending_array = []

        self.Rest_Count = 0
        self.Stop_Time_Factor = 30 #Time interval buggy is stopped

        '''stuff for grid percentage field scanned'''
        self.Pseudo_Past_Position = 0

        '''machine learning rotation stuff'''
        self.Rotation_Angle = 0
        self.Past_X = 0
        self.Past_Y = 0


    def update(self, collision_walls_group_horz_bottom, collision_walls_group_horz_top, collision_walls_group_vert_left, collision_walls_group_vert_right):

        #print (self.Current_Animation)

        '''collision stuff'''
        wall_collision_list_horz_bottom = pygame.sprite.spritecollide(self, collision_walls_group_horz_bottom, False, pygame.sprite.collide_rect_ratio(1))
        wall_collision_list_horz_top = pygame.sprite.spritecollide(self, collision_walls_group_horz_top, False, pygame.sprite.collide_rect_ratio(1))
        wall_collision_list_vert_left = pygame.sprite.spritecollide(self, collision_walls_group_vert_left, False, pygame.sprite.collide_rect_ratio(1))
        wall_collision_list_vert_right = pygame.sprite.spritecollide(self, collision_walls_group_vert_right, False, pygame.sprite.collide_rect_ratio(1))

        Stop_Arg = (self.x2-self.x1)

        if self.Pseudo_Past_Position>self.Buggy_Dimensions:
            self.Field_Scanned_Perc+=self.percentage_per_grid
            self.Pseudo_Past_Position = 0

        if Stop_Arg<0:
            self.Current_Animation = 'Idle'

        if self.Current_Animation=='Idle':

            if self.Navigate_Bool==True:
                self.Navigate_Bool=False
                pos_tuple = (self.Current_X_position, self.Current_Y_position)
                print ('appending to array')
                self.ending_array.append(pos_tuple)

            else:
                pass

        elif self.Current_Animation=='Move_Down':

            self.Navigate_Bool = False

            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, 180)
            self.image.set_colorkey((255,255,255))
            self.Current_Y_position+=self.Buggy_Speed
            self.rect.center = self.Current_X_position, self.Current_Y_position

        elif self.Current_Animation=='Move_Up':

            self.Navigate_Bool = False

            self.image, self.rect = load_image('car.png', 'Car')
            self.image.set_colorkey((255,255,255))
            self.Current_Y_position+=-self.Buggy_Speed
            self.rect.center = self.Current_X_position, self.Current_Y_position

        elif self.Current_Animation=='Move_Left':

            self.Navigate_Bool = False

            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, 90)
            self.image.set_colorkey((255,255,255))
            self.Current_X_position+=-self.Buggy_Speed
            self.rect.center = self.Current_X_position, self.Current_Y_position

        elif self.Current_Animation=='Move_Right':

            self.Navigate_Bool = False

            self.Current_X_position+=self.Buggy_Speed
            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, -90)
            self.image.set_colorkey((255,255,255))
            self.rect.center = self.Current_X_position, self.Current_Y_position

        elif self.Current_Animation=='Navigate_Right':

            self.Navigate_Bool = True

            if self.Rest_Count>10 and self.Rest_Count<self.Stop_Time_Factor:
                self.Current_X_position+=0
            else:
                self.Current_X_position+=self.Buggy_Speed
                self.Pseudo_Past_Position+=self.Buggy_Speed
            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, -90)
            self.image.set_colorkey((255,255,255))
            self.rect.center = self.Current_X_position, self.Current_Y_position

            self.Rest_Count+=1

            if self.Rest_Count == self.Stop_Time_Factor:
                self.Rest_Count = 0

            if self.Current_X_position>self.x2:
                self.Update_Animation('Navigate_Down')

        elif self.Current_Animation=='Navigate_Down':

            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, 180)
            self.image.set_colorkey((255,255,255))
            if self.Rest_Count>10 and self.Rest_Count<self.Stop_Time_Factor:
                self.Current_Y_position+=0
            else:
                self.Current_Y_position+=self.Buggy_Speed
                self.Pseudo_Past_Position+=self.Buggy_Speed
            self.rect.center = self.Current_X_position, self.Current_Y_position

            self.Rest_Count +=1

            if self.Rest_Count == self.Stop_Time_Factor:
                self.Rest_Count = 0

            if self.Current_Y_position>self.y2:
                self.Update_Animation('Navigate_Left')

        elif self.Current_Animation=='Navigate_Left':

            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, 90)
            self.image.set_colorkey((255,255,255))
            if self.Rest_Count>10 and self.Rest_Count<self.Stop_Time_Factor:
                self.Current_X_position+=0
            else:
                self.Current_X_position+=-self.Buggy_Speed
                self.Pseudo_Past_Position+=self.Buggy_Speed
            self.rect.center = self.Current_X_position, self.Current_Y_position

            self.Rest_Count+=1

            if self.Rest_Count == self.Stop_Time_Factor:
                self.Rest_Count = 0

            if self.Current_X_position<self.x1:
                self.x1 = self.x1+self.Buggy_Dimensions
                self.x2 = self.x2-self.Buggy_Dimensions
                self.y1 = self.y1+self.Buggy_Dimensions
                self.y2 = self.y2-self.Buggy_Dimensions
                self.Update_Animation('Navigate_Up')

        elif self.Current_Animation=='Navigate_Up':

            self.image, self.rect = load_image('car.png', 'Car')
            self.image.set_colorkey((255,255,255))
            if self.Rest_Count>10 and self.Rest_Count<self.Stop_Time_Factor:
                self.Current_Y_position+=0
            else:
                self.Current_Y_position+=-self.Buggy_Speed
                self.Pseudo_Past_Position+=self.Buggy_Speed
            self.rect.center = self.Current_X_position, self.Current_Y_position

            self.Rest_Count+=1

            if self.Rest_Count == self.Stop_Time_Factor:
                self.Rest_Count = 0            

            if self.Current_Y_position<self.y1:
                self.Update_Animation('Navigate_Right')

        elif self.Current_Animation=='Machine_Learning_Start':

            self.Navigate_Bool = False

            self.Current_X_position+=self.Buggy_Speed
            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, -90)
            self.image.set_colorkey((255,255,255))
            self.rect.center = self.Current_X_position, self.Current_Y_position

            if len(wall_collision_list_vert_right)!=0:
                for wall in wall_collision_list_vert_right:
                    self.Current_X_position = wall.rect.x - 40
                    self.rect.center = self.Current_X_position, self.Current_Y_position
                self.Current_Animation='Turn Randomly'

        elif self.Current_Animation=='Machine_Learning_After':
            self.Navigate_Bool = False

            self.Current_X_position+=-self.Past_X
            self.Current_Y_position+=-self.Past_Y
            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, self.Rotation_Angle)
            self.image.set_colorkey((255,255,255))
            self.rect.center = self.Current_X_position, self.Current_Y_position

            if len(wall_collision_list_vert_left)!=0 or len(wall_collision_list_horz_bottom)!=0 or len(wall_collision_list_vert_right)!=0 or len(wall_collision_list_horz_top)!=0:
                for wall in wall_collision_list_vert_right:
                    self.Current_X_position = wall.rect.x - 40
                    self.rect.center = self.Current_X_position, self.Current_Y_position
                for wall in wall_collision_list_vert_left:
                    self.Current_X_position = wall.rect.x + 40
                    self.rect.center = self.Current_X_position, self.Current_Y_position
                for wall in wall_collision_list_horz_bottom:
                    self.Current_Y_position = wall.rect.y - 40
                    self.rect.center = self.Current_X_position, self.Current_Y_position
                for wall in wall_collision_list_horz_top:
                    self.Current_Y_position = wall.rect.y + 40
                    self.rect.center = self.Current_X_position, self.Current_Y_position
                self.Current_Animation='Turn Randomly'

        elif self.Current_Animation=='Turn Randomly':

            self.Get_random_angle()

            if self.Rotation_Angle>0 and self.Rotation_Angle<91:
                self.Angle_Factor_Y = (90-self.Rotation_Angle)/90
                self.Angle_Factor_X = self.Rotation_Angle/90
            elif self.Rotation_Angle>90 and self.Rotation_Angle<181:
                self.Angle_Factor_Y = (90-self.Rotation_Angle)/90
                self.Angle_Factor_X = (180-self.Rotation_Angle)/90

            elif self.Rotation_Angle>180 and self.Rotation_Angle<271:
                self.Angle_Factor_Y = (self.Rotation_Angle-270)/90
                self.Angle_Factor_X = (180-self.Rotation_Angle)/90
            elif self.Rotation_Angle>270 and self.Rotation_Angle<361:
                self.Angle_Factor_Y = (self.Rotation_Angle-270)/90
                self.Angle_Factor_X = (self.Rotation_Angle-360)/90

            self.Current_X_position+=-self.Buggy_Speed*self.Angle_Factor_X
            self.Past_X = self.Buggy_Speed*self.Angle_Factor_X

            self.Current_Y_position+=-(self.Buggy_Speed*(self.Angle_Factor_Y))
            self.Past_Y = (self.Buggy_Speed*(self.Angle_Factor_Y))

            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, self.Rotation_Angle)
            self.image.set_colorkey((255,255,255))
            self.rect.center = self.Current_X_position, self.Current_Y_position

            self.Current_Animation='Machine_Learning_After'



        elif self.Current_Animation=='Reset':

            self.Navigate_Bool = False

            self.image, self.rect = load_image('car.png', 'Car')
            self.image.set_colorkey((255,255,255))
            self.rect.center = self.Current_X_position, self.Current_Y_position

        elif self.Current_Animation=='Diagonal':
            self.Navigate_Bool = False

            self.Rotation_Angle = 10

            if self.Rotation_Angle>0 and self.Rotation_Angle<91:
                self.Angle_Factor_Y = (90-self.Rotation_Angle)/90
                self.Angle_Factor_X = self.Rotation_Angle/90
            elif self.Rotation_Angle>90 and self.Rotation_Angle<181:
                self.Angle_Factor_Y = (90-self.Rotation_Angle)/90
                self.Angle_Factor_X = (180-self.Rotation_Angle)/90

            elif self.Rotation_Angle>180 and self.Rotation_Angle<271:
                self.Angle_Factor_Y = (self.Rotation_Angle-270)/90
                self.Angle_Factor_X = (180-self.Rotation_Angle)/90
            elif self.Rotation_Angle>270 and self.Rotation_Angle<361:
                self.Angle_Factor_Y = (self.Rotation_Angle-270)/90
                self.Angle_Factor_X = (self.Rotation_Angle-360)/90


            self.Current_X_position+=-self.Buggy_Speed*self.Angle_Factor_X
            self.Current_Y_position+=-(self.Buggy_Speed*(self.Angle_Factor_Y))
            self.image, self.rect = load_image('car.png', 'Car')
            self.image = pygame.transform.rotate(self.image, self.Rotation_Angle)
            self.image.set_colorkey((255,255,255))
            self.rect.center = self.Current_X_position, self.Current_Y_position


    def Update_Animation(self, var):

        self.Rest_Count = 0

        self.Current_Animation = var

    def Update_Field_Coordinates(self, x1,y1,x2,y2):

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


    def Print_Ending_Array(self):
        print (self.ending_array)

    def Fetch_Field_Percentage_Scanned(self):
        if self.Navigate_Bool==False:
            return '##'
        else:
            rounded_perc = round(self.Field_Scanned_Perc, 2)
            return rounded_perc


    def Get_random_angle(self):
        self.Rotation_Angle = random.randint(0,360) 
