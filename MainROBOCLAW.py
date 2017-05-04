
'''
Author: Ekram
Date: 1.5.17
This will run the roboclaw as a separate script in daemon mode. It will constantly update the variable
text file. And check what its current action should be. This will be read from ROBOCLAW_INSTRUCTION.txt

Memory is being shared for the moment through multiple text files. These are:

ROBOCLAW_INSTRUCTION.txt
ROBOCLAW_VARIABLES.txt
DESTINATION_MEMORY.txt
'''

from roboclaw import *
from Navigation import *
import math
import time


#Global Vars
address = 0x80              #Roboclaw Address
width = ''
radius_wheel = ''

def HsineFunc(Cur_x, Cur_y, dest_x, dest_y):

    '''these are the actual distances in m of both x and y axes of rOS'''
    X_meters = float(2)
    Y_meters = float(1.5)

    Current_X = float(Cur_x)
    Currrent_Y = float(Cur_y)

    Dest_X = float(dest_x)
    Dest_Y = float(dest_y)

    Angle = (math.atan(((Dest_Y - Currrent_Y))/(Dest_X - Current_X)))*(180/math.pi)

    Angle_tan2 = (math.atan2(Dest_Y - Currrent_Y, Dest_X - Current_X))*(180/math.pi)

    if Angle_tan2<0:
        Angle_tan2 = abs(Angle_tan2) + 90
    elif Angle_tan2>90 and Angle_tan2<180:
        Angle_tan2 = Angle_tan2 + 180

    Distance_between_points = math.sqrt((((Dest_X - Current_X)*X_meters)**2) + ((Dest_Y - Currrent_Y)*Y_meters)**2)

    return (Angle_tan2, Distance_between_points)


def AttemptToConnectToRoboClaw():

    '''for windows use COM3'''
    print ('Attempting connection..')
    Open("/dev/ttyACM0",115200)
    print("CONNECTION SUCCESSFUL!")

    SetM1VelocityPID(address, 33377, 471, 0, 992)
    SetM2VelocityPID(address, 23916 , 319, 0, 1040)
    #Motor safe state
    ForwardMixed(address, 0)
    TurnRightMixed(address, 0)

def Update_Rclaw_Var_text_file():
    '''this when called will update the ROBOCLAW_VARIABLES text file with the current readings'''
    M1_Encoder = ReadSpeedM1(address)
    M2_Encoder = ReadSpeedM2(address)

    # M1_Current = ReadCurrents(address)
    # M2_Current = ReadCurrents(address)

    # M1_Temp = ReadTemp2(address)

    #Write all these into txt file ROBOCLAW_VARIABLES.txt
    with open('ROBOCLAW_VARIABLES.txt', 'w') as f2:
        #print ('Writing to ROBOCLAW_VARIABLES.txt file..')
        f2.write(str(M1_Encoder[1]) + ',' + str(M2_Encoder[1])) #for now writing only encoders

def Main():

    Curr_X = 0
    Curr_Y = 0

    past_encoder1 = 0
    past_encoder2 = 0
    past_encoder_orient = 0

    past_encoder_x = 0
    past_encoder_y = 0

    width = float(0.2)
    radius_wheel = float(0.08)


    ResetEncoders(address)

    #Enter daemon mode, no loop rate set for now
    while True:
        #Read the instruction text file
        with open('ROBOCLAW_INSTRUCTION.txt', 'r') as f: 
            instruction_list = f.read().splitlines() #possible instructions: Update_var, P2P_NAV, Perim_Nav
            try:
                current_instruction = instruction_list[0]
            except:
                current_instruction = 'STOP'

        if current_instruction=='Update_var':

            Update_Rclaw_Var_text_file()

        elif current_instruction=='Angle_Test':

            #Get Current Co-ordinates from reading text file 
            with open('GPS_TEXT.txt', 'r') as f: 
                data = f.read().splitlines()
                try:
                    data_split = data[0].split(',')
                except IndexError:
                    pass

                Curr_X = float(data_split[0])
                Curr_Y = float(data_split[1])

                Curr_Orient = float(data_split[2])

                if Curr_Orient<float(-90) and Curr_Orient>float(-180):
                    Curr_Orient = Curr_Orient+float(450)
                else:
                    Curr_Orient = Curr_Orient + float(90)

                print (Curr_Orient)

        elif current_instruction=='Super_easy_hacky_nav':

            Update_Rclaw_Var_text_file()

            Dest_X = float(0)
            Dest_Y = float(1)

            #Get Current Co-ordinates from reading text file 
            with open('GPS_TEXT.txt', 'r') as f: 
                data = f.read().splitlines()
                try:
                    data_split = data[0].split(',')
                except IndexError:
                    pass

                Curr_X = float(data_split[0])
                Curr_Y = float(data_split[1])

                Curr_Orient = float(data_split[2])

                if Curr_Orient<float(-90) and Curr_Orient>float(-180):
                    Curr_Orient = Curr_Orient+float(450)
                else:
                    Curr_Orient = Curr_Orient + float(90)


            response = HsineFunc(Curr_X, Curr_Y, Dest_X, Dest_Y)
            Target_Angle = float(response[0])
            Target_Distance = float(response[1])

            #make buggy turn about point until it faces the destination
            while True:
                ForwardM1(address, 30)         
                BackwardM2(address, 30)

                #Get Current Co-ordinates from reading text file 
                with open('GPS_TEXT.txt', 'r') as f: 
                    data = f.read().splitlines()
                    try:
                        data_split = data[0].split(',')
                    except IndexError:
                        pass


                    Curr_Orient = float(data_split[2])

                    if Curr_Orient<float(-90) and Curr_Orient>float(-180):
                        Curr_Orient = Curr_Orient+float(450)
                    else:
                        Curr_Orient = Curr_Orient + float(90)


                    print ('Current ANGLE IS: ' + str(Curr_Orient))
                    print ('Destination ANGLE IS: ' + str(Target_Angle))
                    print ('')
                    print ('---------------------------------------------')

                if Target_Angle>(Curr_Orient*0.9) and Target_Angle<(Curr_Orient*1.1):
                    break

                time.sleep(0.1)

            print ('Buggy is now roughly facing its destination')
            print ('Now buggy will move this much meteres in a straight line: ' + str(Target_Distance))


            #now make the buggy go straight towards it

            encoder_distance = int(Target_Distance*float(1350))
            print (encoder_distance)

            SpeedDistanceM1(address, 500, encoder_distance, 1)
            SpeedDistanceM2(address, 500, encoder_distance, 1)

            time.sleep(3)
            while True:

                speedEncoder = ReadSpeedM1(address)
                m2 = ReadSpeedM2(address)
                print (speedEncoder)
                print (m2)

                if speedEncoder[1]==0:
                    break
            
            ForwardM1(address, 0)
            ForwardM2(address, 0)

            with open('ROBOCLAW_INSTRUCTION.txt', 'w') as f2:
                f2.write('STOP')


        elif current_instruction=='Distance_Test':

            SpeedDistanceM1(address, 500, 3000, 1)
            SpeedDistanceM2(address, 500, 3000, 1)

            with open('ROBOCLAW_INSTRUCTION.txt', 'w') as f2:
                f2.write('STOP')

        elif current_instruction=='P2P_NAV':

            Update_Rclaw_Var_text_file()

            #Commence navigation algorithm here
            #First get all the destination co ords from destination_memory.txt
            # with open('DESTINATION_MEMORY.txt', 'r') as f1: 
            #     content_list = f1.read().splitlines()
            #     content_list_splitted = content_list[0].split(',')

            #     Dest_X = float(content_list_splitted[0])
            #     Dest_Y = float(content_list_splitted[1])
            #     lv_gain = float(content_list_splitted[2])
            #     av_gain = float(content_list_splitted[3])
            #     Dest_margin = float(content_list_splitted[4])

            Dest_X = float(0.957)
            Dest_Y = float(0.097)
            lv_gain = float(0.01)
            av_gain = float(0.1)
            Dest_margin = float(0.2)


            #Get Current Co-ordinates from reading text file 
            with open('GPS_TEXT.txt', 'r') as f: 
                data = f.read().splitlines()
                try:
                    data_split = data[0].split(',')
                except IndexError:
                    pass

                if float(abs(float(data_split[0])))!=float(10):
                    Curr_X = float(data_split[0])
                    print ('X : ' + str(Curr_X))
                    Curr_Y = float(data_split[1])
                    print ('Y : ' + str(Curr_Y))
                    Curr_Orient = float(data_split[2])
                else: 
                    print ('Something wrong with ROS, x and y set to previous values..')

                if Curr_Orient<float(-90) and Curr_Orient>float(-180):
                    Curr_Orient = Curr_Orient+float(450)
                else:
                    Curr_Orient = Curr_Orient + float(90)

                Curr_Orient_in_Rads = Curr_Orient*(math.pi/180)
                print ('ANGLE IN RADS: ' + str(Curr_Orient_in_Rads))

            response = MainNav(Curr_X, Curr_Y, Curr_Orient_in_Rads, Dest_X, Dest_Y, lv_gain, av_gain, Dest_margin)

            if response=='STOP':
                print ('STOPPING********************************************************************')
                with open('ROBOCLAW_INSTRUCTION.txt', 'w') as f2:
                    f2.write('STOP')
                continue
            else:
                linear_velocity = float(0.02)#response[0]
                angular_velocity = response[1]

                output = ConvertTotalVelocityToMotorSpeeds(linear_velocity, angular_velocity, width, radius_wheel)
                right_motor = int(output[0])
                print ('Speed M2 : ' + str(ReadSpeedM2(address)[1]))
                print ('Calculated M2 : ' + str(right_motor))

                left_motor = int(output[1])
                print ('Speed M1 : ' + str(ReadSpeedM1(address)[1]))
                print ('Calculated M1 : ' + str(left_motor))
                print ('----------------------------')

                SpeedM1(address, left_motor)
                SpeedM2(address, right_motor)

            time.sleep(0.1)

        elif current_instruction=='EncoderP2P_NAV':

            Update_Rclaw_Var_text_file()

            #Get Current Co-ordinates past encoders are initialised at 0 
            M1_Encoder = float(ReadEncM1(address)[1])
            M2_Encoder = float(ReadEncM2(address)[1])

            Delta_M1_Enc = (M1_Encoder - past_encoder1)/1250
            Delta_M2_Enc = (M2_Encoder - past_encoder2)/1250


            avg_distance = (Delta_M1_Enc + Delta_M2_Enc)/2

            past_encoder1 = M1_Encoder
            past_encoder2 = M2_Encoder

            Current_Orientation = past_encoder_orient + (Delta_M2_Enc - Delta_M1_Enc)/width

            Current_Orientation = Current_Orientation - (2*math.pi*math.floor((Current_Orientation+math.pi)/(2*math.pi)))

            Current_X = past_encoder_x + (avg_distance*math.cos(past_encoder_orient+(0.5*Current_Orientation)))
            Current_Y = past_encoder_y + (avg_distance*math.sin(past_encoder_orient+(0.5*Current_Orientation)))

            past_encoder_x = Current_X
            past_encoder_y = Current_Y
            past_encoder_orient = Current_Orientation

            print ('x: ' + str(Current_X))
            print ('y: ' + str(Current_Y))
            print ('theta: ' + str(Current_Orientation))
            print ('Motor 1 Encoder: ' + str(M1_Encoder))
            print ('Motor 2 Encoder: ' + str(M2_Encoder))

            response = MainNav(Current_X, Current_Y, Current_Orientation, 1, 0 , 0.1, 0.1, 0.1)

            print ('')
            print ('--------------------------------------')

            if response=='STOP':
                print ('STOPPING********************************************************************')
                with open('ROBOCLAW_INSTRUCTION.txt', 'w') as f2:
                    f2.write('STOP')
                continue

            else:
                linear_velocity = response[0]
                angular_velocity = response[1]

                output = ConvertTotalVelocityToMotorSpeeds(linear_velocity, angular_velocity, 0.2, 0.08)

                right_motor = int(output[0])
                left_motor = int(output[1])


                SpeedM1(address, right_motor)
                SpeedM2(address, left_motor)

            time.sleep(0.5)

        elif current_instruction=='Perim_Nav':

            Update_Rclaw_Var_text_file()

            #Commence perimeter navigation algorithm here

        elif current_instruction=='FORWARD':

            Update_Rclaw_Var_text_file()

            ForwardM1(address, 64)         
            ForwardM2(address, 64)

        elif current_instruction=='BACKWARD':

            Update_Rclaw_Var_text_file()

            BackwardM1(address, 64)         
            BackwardM2(address, 64)

        elif current_instruction=='LEFT':

            Update_Rclaw_Var_text_file()

            BackwardM1(address, 64)         
            ForwardM2(address, 64)

        elif current_instruction=='RIGHT':

            Update_Rclaw_Var_text_file()

            ForwardM1(address, 64)         
            BackwardM2(address, 64)

        elif current_instruction=='STOP':

            Update_Rclaw_Var_text_file()

            ForwardM1(address, 0)         
            ForwardM2(address, 0)

        else:
            Update_Rclaw_Var_text_file()
            #make motors do nothing
            ForwardM1(address, 0)         
            ForwardM2(address, 0)





if __name__ == '__main__':
    print ('Setting current Roboclaw instruction to only update variable text file.. ')
    with open('ROBOCLAW_INSTRUCTION.txt', 'w') as f2:
        f2.write('P2P_NAV')
    print ('Attempting to connect to roboclaw..')
    AttemptToConnectToRoboClaw()
    print ('Starting main daemon script..')
    Main()
