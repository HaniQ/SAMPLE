#Created by Sam
#Edited by Ekram VERSION1 3rd week final code
# I dunno if on_message has to be called inside the while loop or if it will keep looping in the background with loop_start() function
#Need a lot of tests with it to see if values from inside are being properly passed to the main loop
#mqtt-roboclaw.py and roboclaw.py should both be placed inside /home/pi of the receiver pi intended to go on the buggy
#RUN mqtt-roboclaw.py

import httplib, urllib
import time
import roboclaw
from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import serial
import sys
import RPi.GPIO as GPIO     # Library to set up ports for sensors

key = '4PNC5PRP910FDCIR'  # Thingspeak channel to update

#Global Vars
address = 0x80              #Roboclaw Address
Global_Distance = 1         #Global variable for distance

topic="ds4"                 # MQTT broker topic
user="sam"                  # MQTT broker user
pw="mosquitto1894"          # MQTT broker password
host="130.88.154.7"         # MQTT broker host
port=1894                   # MQTT broker port
value="123"                 # somethin i need for myapp

#Ultrasound trig and echo pins
TRIG=23
ECHO=24

#Light colour values for sense_hat
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (200,50,50)
white = (255,255,255)


#Sense Hat stuff
sense = SenseHat()
sense.clear()

#Arrow LED Up,down,left right for sense Hat
Arrow_UP=[  white, white, white, white, white, white, white, white,
            white, white, white, red, red, white, white, white,
            white, white, red, red, red, red, white, white,
            white, white, red, red, red, red, red, white,
            white, white, white, red, red, white, white, white,
            white, white, white, red, red, white, white, white,
            white, white, white, red, red, white, white, white,
            white, white, white, red, red, white, white, white
]

Arrow_DOWN= [   white, white, white, red, red, white, white, white,
                white, white, white, red, red, white, white, white,
                white, white, white, red, red, white, white, white,
                white, white, white, red, red, white, white, white,
                white, white, white, red, red, white, white, white,
                white, red, red, red, red, white, white, white,
                white, white, red, red, red, white, white, white,
                white, white, white, red, red, white, white, white
]

Arrow_RIGHT= [  white, white, white, white, white, white, white, white,
                white, white, white, white, red, white, white, white,
                white, white, white, white, red, red, white, white,
                red, red, red, red, red, red, red, white,
                red, red, red, red, red, red, red, white,
                white, white, white, white, red, red, white, white,
                white, white, white, white, red, white, white, white,
                white, white, white, white, white, white, white, white
]

Arrow_LEFT= [   white, white, white, white, white, white, white, white,
                white, white, white, red, white, white, white, white,
                white, white, red, red, white, white, white, white,
                white, red, red, red, red, red, red, red,
                white, red, red, red, red, red, red, red,
                white, white, red, red, white, white, white, white,
                white, white, white, red, white, white, white, white,
                white, white, white, white, white, white, white, white
]
#--------------------------------------------------------------------------------


#Roboclaw stuff--------------------------------
#Windows comport name
#roboclaw.Open("COM3",115200)
#Linux comport name
def AttemptToConnectToRoboClaw():
    try:
        roboclaw.Open("/dev/ttyACM0",115200)
        #Motor safe state
        roboclaw.ForwardMixed(address, 0)
        roboclaw.TurnRightMixed(address, 0)
        sense.set_pixel(1, 7, green)
    except Exception as e:
        print("problem with roboclaw")
        print e
        sense.set_pixel(1, 7, red)



def on_connect(mqttc, userdata, rc):
    print('connected...rc=' + str(rc))
    mqttc.subscribe(topic, qos=0)
    sense.set_pixel(0, 7, green)

def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))
    sense.set_pixel(0, 7, red)

def on_message(mqttc, userdata, msg):
    print('message received...')
    print('topic: ' + msg.topic + ', qos: ' + 
        str(msg.qos) + ', message: ' + str(msg.payload))

    if(msg.topic == 'ds4') and (msg.payload == 'Down'):
        print ('Down received')
        sense.set_pixels(Arrow_DOWN)
        try:
            roboclaw.BackwardM2(address, 32)
            roboclaw.BackwardM1(address, 32)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()


    if(msg.topic == 'ds4') and (msg.payload == 'Left'):
        print ('Left received')
        sense.set_pixels(Arrow_LEFT)
        try:
            roboclaw.ForwardM1(address, 32)
            roboclaw.ForwardM2(address, 64)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()

        
    if(msg.topic == 'ds4') and (msg.payload == 'Right'):
        print ('Right received')
        sense.set_pixels(Arrow_RIGHT)
        try:
            roboclaw.ForwardM1(address, 64 )
            roboclaw.ForwardM2(address, 32)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()


    if(msg.topic == 'ds4') and (msg.payload == 'UP'):           # ultra-sound proximity will pass distance to Global_Distance which will let 
        print ('UP received')                                   #the manual control only press forwards IF Global_Distance is more than 500cm
        sense.set_pixels(Arrow_UP)
        if Global_Distance>500:
            try:
                roboclaw.ForwardM1(address, 32)
                roboclaw.ForwardM2(address, 32)
            except:
                print("problem with roboclaw")
                sense.set_pixel(1, 7, red)
                AttemptToConnectToRoboClaw()
        else :
            roboclaw.ForwardM1(address, 0)
            roboclaw.ForwardM2(address, 0)    

    if(msg.topic == 'ds4') and (msg.payload == 'Triangle'):
        print ('Triangle received')
        sense.set_pixel(7, 0, white)
        try:
            roboclaw.ForwardM1(address, 0)
            roboclaw.ForwardM2(address, 0)
        except:
            print("problem with roboclaw")
            sense.set_pixel(1, 7, red)
            AttemptToConnectToRoboClaw()
            


def on_subscribe(mqttc, userdata, mid, granted_qos):
    print('subscribed (qos=' + str(granted_qos) + ')')

def on_unsubscribe(mqttc, userdata, mid, granted_qos):
    print('unsubscribed (qos=' + str(granted_qos) + ')')



AttemptToConnectToRoboClaw()

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
mqttc.username_pw_set(user,pw)
mqttc.connect(host, port, 10)
mqttc.loop_start() #start threaded


#MAIN PROGRAM LOOP TO BE LOOPING INSIDE THE BUGGY
while True:
    #Set up readings from roboclaw to be sent to thingspeak
    M1_Speed = roboclaw.readM1speed()
    M2_Speed = roboclaw.readM2speed()
    (M1_Current,M2_Current) = roboclaw.readcurrents()
    Roboclaw_Temperature = roboclaw.readtemparature()
    Main_Battery = roboclaw.readmainbattery()
    
    #---------------------------------Ultrasound loop code:------------------------------#
    GPIO.setmode(GPIO.BCM)

    TRIG = 23 
    ECHO = 24

    print "Distance Measurement In Progress"

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    print "Waiting For Sensor To Settle"
    time.sleep(1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print "Distance:",distance,"cm"
    
    Global_Distance = distance                      #Setting up global distance variable to be passed as argument for forward motion

    
    #--------------------Ultrasound main loop code end---------------------------------------#
    
    #---------------Thingspeak main bulk code which will send all 7 values to the website---------------------#
    params = urllib.urlencode({'field1': distance,'field2': M1_Speed,'field3': M2_Speed,'field4': M1_Current,'field5': M2_Current,'field6':Roboclaw_Temperature,'field7':Main_Battery,'key':key }) 
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print distance
        print response.status, response.reason
        data = response.read()
        conn.close()
    except:
        print "connection failed"
        
    GPIO.cleanup()
    #-----------------Thingspeak code end-------------------------------#
    
    

    

