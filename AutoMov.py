#Importing all the relevant stuff
import time
import sys
import RPi.GPIO as GPIO
import roboclaw
from flask import Flask, render_template, request, url_for
from decimal import *

StartLat = 0
StartLong = 0

EndLat = 0
EndLong = 0

#Buggy Size Constant
BuggyLengthLat = 0.00056
BuggyWidthLong = 0.007897

#Proportional constants
KpLat = 1
KpLong = 1
FlatMotorValue = 50
ScaleErrorFactor = 100

def CompassDegree():    #This function will return a degree from 0 to 360 with 0/360 being north and 90 being east
    Angle = 0
    return Angle


def AlignNorth():       
    CurrentDirection = CompassDegree()
    #Move motors to get to 0 degree
    
def AlignEast():       
    CurrentDirection = CompassDegree()
    #Move motors to get to 90 degree
    
def AlignSouth():      
    CurrentDirection = CompassDegree()
    #Move motors to get to 180 degree
    
def AlignWest():       #This function will
    CurrentDirection = CompassDegree()
    #Move motors to get to 270 degree
    

#East and West mean right and left and north and south mean forward and backward on specific frames
def MapMotion(value1,value2):
    
    StartLat = 50       #This values will be obtained from GPS module and will be different each time this loop iterates
    StartLong = 60
    
    EndLat = value1
    EndLong = value2
    
    Align = CompassDegree()             #This gives the degree which implies which direction tank is facing at start
    
    
    if( (0<=Align<=45) or (315<=Align<=359) ):  #THIS TELLS THE BUGGY THAT ITS FRONT IS FACING NORTH
        print ("FRONT OF TANK FACING NORTH")
        print ("FRONT OF TANK FACING NORTH")
        print ("FRONT OF TANK FACING NORTH")
        
        while ( (0.90*EndLat)<=StartLat<=(1.1*EndLat) and (0.90*EndLong)<=StartLong<=(1.1*EndLong) ): #Main argument is checking if starting co-ordinates come to within +-2% of destination co-ordinates
            
            if(StartLat<EndLat):        #GO NORTH
                
                if( StartLong<EndLong ):      #GO NORTH EAST
                    ForwardM1*(EndLat-StartLat)*KpLat*(EndLong-StartLong)*KpLong*FlatMotorValue
                    ForwardM2*(EndLat-StartLat)*KpLat*FlatMotorValue
                    print ("GO NORTH EAST")
                    
                elif( StartLong>EndLong ):     #GO NORTH WEST 
                    ForwardM1*(EndLat-StartLat)*KpLat*FlatMotorValue
                    ForwardM2*(EndLat-StartLat)*KpLat*(StartLong-EndLong)*KpLong*FlatMotorValue
                    print ("GO NORTH WEST")
                    
                elif( (0.9*EndLong)<=StartLong<=(1.1*EndLong) ):     #GO ONLY NORTH
                    ForwardM1*(EndLat-StartLat)*KpLat*FlatMotorValue
                    ForwardM2*(EndLat-StartLat)*KpLat*FlatMotorValue
                    print ("GO ONLY NORTH")
                    
            elif(StartLat>EndLat):      #GO SOUTH
                
                if( StartLong<EndLong ):      #GO SOUTH EAST
                    BackwardM1*(StartLat-EndLat)*KpLat*(EndLong-StartLong)*KpLong*FlatMotorValue
                    BackwardM2*(StartLat-EndLat)*KpLat*FlatMotorValue
                    print ("GO SOUTH EAST")
                    
                elif( StartLong>EndLong ):     #GO SOUTH WEST 
                    BackwardM1*(StartLat-EndLat)*KpLat*FlatMotorValue
                    BackwardM2*(StartLat-EndLat)*KpLat*(StartLong-EndLong)*KpLong*FlatMotorValue
                    print ("GO SOUTH WEST")
                    
                elif( (0.9*EndLong)<=StartLong<=(1.1*EndLong) ):     #GO ONLY SOUTH
                    BackwardM1*(StartLat-EndLat)*KpLat*FlatMotorValue
                    BackwardM2*(StartLat-EndLat)*KpLat*FlatMotorValue
                    print ("GO ONLY SOUTH")
                    
            elif((0.9*EndLat)<=StartLat<=(1.1*EndLat)):   #Do not go south or north/ go only east/west
                
                if( StartLong<EndLong ):
                    MakeWideArcToGoEast
                    print ("GO EAST ONLY")
                    
                elif( StartLong>EndLong ):
                    MakeWideArcToGoWest
                    print ("GO WEST ONLY")
                    
#--------------------------------------------------------------------------------------------------------------------#
                    
    elif (135<=Align<=225):  #THIS TELLS THE BUGGY THAT ITS FRONT IS FACING SOUTH
        print ("FRONT OF TANK FACING SOUTH")
        print ("FRONT OF TANK FACING SOUTH")
        print ("FRONT OF TANK FACING SOUTH")
        
        while ( (0.9*EndLat)<=StartLat<=(1.1*EndLat) and (0.9*EndLong)<=StartLong<=(1.1*EndLong) ): #Main argument is checking if starting co-ordinates come to within +-2% of destination co-ordinates
            
            if(StartLat>EndLat):        #GO NORTH
                
                if( StartLong>EndLong ):      #GO NORTH EAST
                    ForwardM1*(StartLat-EndLat)*KpLat*(StartLong-EndLong)*KpLong*FlatMotorValue
                    ForwardM2*(StartLat-EndLat)*KpLat*FlatMotorValue
                    print ("GO NORTH EAST")
                    
                elif( StartLong<EndLong ):     #GO NORTH WEST 
                    ForwardM1*(StartLat-EndLat)*KpLat*FlatMotorValue
                    ForwardM2*(StartLat-EndLat)*KpLat*(EndLong-StartLong)*KpLong*FlatMotorValue
                    print ("GO NORTH WEST")
                    
                elif( (0.9*EndLong)<=StartLong<=(1.1*EndLong) ):     #GO ONLY NORTH
                    ForwardM1*(StartLat-EndLat)*KpLat*FlatMotorValue
                    ForwardM2*(StartLat-EndLat)*KpLat*FlatMotorValue
                    print ("GO ONLY NORTH")
                    
            elif(StartLat<EndLat):      #GO SOUTH
                
                if( StartLong>EndLong ):      #GO SOUTH EAST
                    BackwardM1*(EndLat-StartLat)*KpLat*(StartLong-EndLong)*KpLong*FlatMotorValue
                    BackwardM2*(EndLat-StartLat)*KpLat*FlatMotorValue
                    print ("GO SOUTH EAST")
                    
                elif( StartLong<EndLong ):     #GO SOUTH WEST 
                    BackwardM1*(EndLat-StartLat)*KpLat*FlatMotorValue
                    BackwardM2*(EndLat-StartLat)*KpLat*(EndLong-StartLong)*KpLong*FlatMotorValue
                    print ("GO SOUTH WEST")
                    
                elif( (0.9*EndLong)<=StartLong<=(1.1*EndLong) ):     #GO ONLY SOUTH
                    BackwardM1*(EndLat-StartLat)*KpLat*FlatMotorValue
                    BackwardM2*(EndLat-StartLat)*KpLat*FlatMotorValue
                    print ("GO ONLY SOUTH")
        
#--------------------------------------------------------------------------------------------------------------------#
        
    elif (45<=Align<=135):  #THIS TELLS THE BUGGY THAT ITS FRONT IS FACING EAST (All comments in this loop takes facing east as being north)
        print ("FRONT OF TANK FACING EAST")
        print ("FRONT OF TANK FACING EAST")
        print ("FRONT OF TANK FACING EAST")
        
        while ( (0.9*EndLat)<=StartLat<=(1.1*EndLat) and (0.9*EndLong)<=StartLong<=(1.1*EndLong) ): #Main argument is checking if starting co-ordinates come to within +-2% of destination co-ordinates
            
            if(StartLong<EndLong):        #GO NORTH
                
                if( StartLat<EndLat ):      #GO NORTH WEST
                    ForwardM1*(EndLong-StartLong)*KpLat*FlatMotorValue
                    ForwardM2*(EndLong-StartLong)*KpLat*(EndLat-StartLat)*KpLong*FlatMotorValue
                    print ("GO NORTH WEST")
                    
                elif( StartLat>EndLat ):     #GO NORTH EAST
                    ForwardM1*(EndLong-StartLong)*KpLat*(StartLat-EndLat)*KpLong*FlatMotorValue
                    ForwardM2*(EndLong-StartLong)*KpLat*FlatMotorValue
                    print ("GO NORTH EAST")
                    
                elif( (0.9*EndLat)<=StartLat<=(1.1*EndLat) ):     #GO ONLY NORTH
                    ForwardM1*(EndLong-StartLong)*KpLat*FlatMotorValue
                    ForwardM2*(EndLong-StartLong)*KpLat*FlatMotorValue
                    print ("GO ONLY NORTH")
                    
            elif(StartLong>EndLong):      #GO SOUTH
                
                if( StartLat<EndLat ):      #GO SOUTH WEST
                    BackwardM1*(StartLong-EndLong)*KpLat*FlatMotorValue
                    BackwardM2*(StartLong-EndLong)*KpLat*(EndLat-StartLat)*KpLong*FlatMotorValue
                    print ("GO SOUTH WEST")
                    
                elif( StartLat>EndLat):     #GO SOUTH EAST
                    BackwardM1*(StartLong-EndLong)*KpLat*(StartLat-EndLat)*KpLong*FlatMotorValue
                    BackwardM2*(StartLong-EndLong)*KpLat*FlatMotorValue
                    print ("GO SOUTH EAST")
                    
                elif( (0.9*EndLat)<=StartLat<=(1.1*EndLat) ):     #GO ONLY SOUTH
                    BackwardM1*(StartLong-EndLong)*KpLat*FlatMotorValue
                    BackwardM2*(StartLong-EndLong)*KpLat*FlatMotorValue
                    print ("GO ONLY SOUTH")
                    
            
                    
#--------------------------------------------------------------------------------------------------------------------#
        
    elif (225<=Align<=315):  #THIS TELLS THE BUGGY THAT ITS FRONT IS FACING WEST
        print ("FRONT OF TANK FACING WEST")
        print ("FRONT OF TANK FACING WEST")
        print ("FRONT OF TANK FACING WEST")
        
        while ( (0.9*EndLat)<=StartLat<=(1.1*EndLat) and (0.9*EndLong)<=StartLong<=(1.1*EndLong) ): #Main argument is checking if starting co-ordinates come to within +-2% of destination co-ordinates
            
            if(StartLong>EndLong):        #GO NORTH
                
                if( StartLat<EndLat ):      #GO NORTH EAST
                    ForwardM1*(EndLong-StartLong)*KpLat*(EndLat-StartLat)*KpLong*FlatMotorValue
                    ForwardM2*(EndLong-StartLong)*KpLat*FlatMotorValue
                    print ("GO NORTH WEST")
                    
                elif( StartLat>EndLat ):     #GO NORTH WEST
                    ForwardM1*(EndLong-StartLong)*KpLat*FlatMotorValue
                    ForwardM2*(EndLong-StartLong)*KpLat*(StartLat-EndLat)*KpLong*FlatMotorValue
                    print ("GO NORTH EAST")
                    
                elif( (0.9*EndLat)<=StartLat<=(1.1*EndLat) ):     #GO ONLY NORTH
                    ForwardM1*(EndLong-StartLong)*KpLat*FlatMotorValue
                    ForwardM2*(EndLong-StartLong)*KpLat*FlatMotorValue
                    print ("GO ONLY NORTH")
                    
            elif(StartLong<EndLong):      #GO SOUTH
                
                if( StartLat<EndLat ):      #GO SOUTH EAST
                    BackwardM1*(StartLong-EndLong)*KpLat*(EndLat-StartLat)*KpLong*FlatMotorValue
                    BackwardM2*(StartLong-EndLong)*KpLat*FlatMotorValue
                    print ("GO SOUTH WEST")
                    
                elif( StartLat>EndLat):     #GO SOUTH WEST
                    BackwardM1*(StartLong-EndLong)*KpLat*FlatMotorValue
                    BackwardM2*(StartLong-EndLong)*KpLat*(StartLat-EndLat)*KpLong*FlatMotorValue
                    print ("GO SOUTH EAST")
                    
                elif( (0.9*EndLat)<=StartLat<=(1.1*EndLat) ):     #GO ONLY SOUTH
                    BackwardM1*(StartLong-EndLong)*KpLat*FlatMotorValue
                    BackwardM2*(StartLong-EndLong)*KpLat*FlatMotorValue
                    print ("GO ONLY SOUTH")
                    
#-------------------------------------------------------------------------------------------------------------------#
                
def RectMapMotion(v1Lat, v1Long, v2Lat,v2Long, v3Lat,v3Long, v4Lat, v4Long):

    #Go to vertex 2 co-ordinate
    MapMotion(v2Lat, v2Long)
    
    #Align the tank to face east
    AlignEast()
    
    #Go to vertex 3 co-ordinate
    MapMotion(v3Lat, v3Long)
    
    #Align the tank to face South
    AlignSouth()
    
    #Go to vertex 4 co-ordinate
    MapMotion(v4Lat, v4Long)
    
    #Align the map to face west
    AlignWest()
    
    #Go to vertex 1 but stop a distance of width of buggy before reaching it
    MapMotion( (v1Lat) , (v1Long-BuggyWidthLong) )
    
    
def SpiralRectMapMotion():
    
    #Get all 4 co-ordinates of vertexes of starting rectangle
    Currentv1Lat = 50
    Currentv1Long = 50
    
    Currentv2Lat = 100
    Currentv2Long = 100
    
    Currentv3Lat = 200
    Currentv3Long = 150
    
    Currentv4Lat = 150
    Currentv4Long = 250
    
    #Find centre of rectangle
    
    #Go to vertex 1 co-ordinates
    MapMotion(current1Lat, current2Long)
    
    #Align the tank to face north
    AlignNorth()
    
    while True: #(buggy's current startinglat/startinglong is not within range of centre of rectangle):
        
        #Find current startnglat/long of buggy through gps
        
        #Make the buggy spiral it once
        RectMapMotion(Currentv1Lat,Currentv1Long,Currentv2Lat,Currentv2Long,Currentv3Lat,Currentv3Long,Currentv4Lat,Currentv4Long)
        
        AlignNorth()
        
        #Create vertexes of new smaller rectangle
        Currentv1Lat = Currentv1Lat - BuggyLengthLat
        Currentv1Long = Currentv1Long - BuggyWidthLong
        
        Currentv2Lat = Currentv2Lat - BuggyLengthLat
        Currentv2Long = Currentv2Long - BuggyWidthLong
        
        Currentv3Lat = Currentv3Lat - BuggyLengthLat
        Currentv3Long = Currentv3Long - BuggyWidthLong
        
        Currentv4Lat = Currentv4Lat - BuggyLengthLat
        Currentv4Long = Currentv4Long - BuggyWidthLong
        
        #Loop back up again with this smaller rectangle
    
    
    
    
                
                
                
                
                
                
                
                
                
                
                
                
        
    
