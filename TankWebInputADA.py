'''
Author: Ekram
Made 30/10/2016
Roboclaw stuff was copy pasted from Sam's code
Using python web flask framework, html and javascript and a little jquery
THIS DOES NOT HAVE PROXIMITY SENSING YET SO PROCEED WITH CAUTION
WORK LEFT: Adding sqlite to fetch proximity readings from the Monitor_values table in t8.db and use that as argument to limit motion of the tank
VERY IMPORTANT: BEFORE RUNNING THIS MAKE SURE ALL THE ROOT WEBPAGE ADDRESS IN THIS CODE MATCHES WITH THE pi's IP ADDRESS
DO NOT tamper with the voice recognition stuff or go to the web page while code is running. It does not have any catch/motor limiters so might make buggy go haywire with stray voice commands
'''

#Importing all the relevant stuff
import time
import sys
import RPi.GPIO as GPIO
import roboclaw
from flask import Flask, render_template, request, url_for
from decimal import *
import sqlite3 as db
from math import*


#Global Vars
address = 0x80              #Roboclaw Address


# Initialize the Flask application
app = Flask(__name__)

LATpy = 0
LONGpy = 0
FinalStartLong = 0
FinalStartLat = 0

#----Roboclaw connection function-----------#
def AttemptToConnectToRoboClaw():
    try:
        roboclaw.Open("/dev/ttyACM0",115200)
        #Motor safe state
        roboclaw.ForwardMixed(address, 0)
        roboclaw.TurnRightMixed(address, 0)
       
    except Exception as e:
        print("problem with roboclaw")
       

# Define a route for root webpage. This is root so this webpage will be output to whoever goes to address http://localhost:5000 (localhost= pi IP address)
@app.route('/')
def index():
    return render_template('index.html')

#Root webpage to display manual buttons for the roboclaw
@app.route('/DBUTTONS')
def DBUTTONS():
    return render_template('Rclaw_main.html')

# Define a route for the action of the form, for example '/ManualF/' NOTE THAT THIS IS ONLY FOR FORWARD MOVEMENT, FOR BACKWARD COPY PASTE THIS WITH FORWARD CHANGED TO BACKWARD
@app.route('/ManualF/', methods=['POST'])
def ManualF():
    Mvar1=request.form['Motor1']                #Accepting both motor value input from the web page as a string
    Mvar2=request.form['Motor2']
    
    newt1 = int(Mvar1)                           #Converting both accepted string numbers into integers, they are still percentage tho
    newt2 = int(Mvar2)
    
    Actual_M1 = newt1*1.27                  #Converting % into actual values from 0 to 127 scale
    Actual_M2 = newt2*1.27
    
    print(Actual_M1)
    print(Actual_M2)
 
    if (Actual_M1>0):
        try:
            roboclaw.ForwardM1(address, int(Round(Actual_M1)))         #Slotting in the two motor integer values into roboclaw forward functio
        except:
            print("problem with roboclaw")
            AttemptToConnectToRoboClaw()
    elif (Actual_M1<0):
        try:
            roboclaw.BackwardM1(address, int(abs(Round(Actual_M1))))
        except:
            print("problem with roboclaw")
            AttemptToConnectToRoboClaw()
    if(Actual_M2>0):
        try:
            roboclaw.ForwardM2(address, int(Round(Actual_M2)))
        except:
            print("problem with roboclaw")
            AttemptToConnectToRoboClaw()
    elif (Actual_M2<0):
        try:
            roboclaw.BackwardM2(address, int(abs(Round(Actual_M2))))
        except:
            print("problem with roboclaw")
            AttemptToConnectToRoboClaw()
          
#This webpage will be returned when the user presses submit button, the location.href function redirects the page back to rclaw_main.html so this is a placeholder page    
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
'''

# Define a route for the action of the form, for example '/ManualF/' NOTE THAT THIS IS ONLY FOR FORWARD MOVEMENT, FOR BACKWARD COPY PASTE THIS WITH FORWARD CHANGED TO BACKWARD
@app.route('/ManualCL/', methods=['POST'])
def ManualCL():
    MvarCL1=request.form['Motor1CL']                #Accepting both motor value input from the web page as a string
    MvarCL2=request.form['Motor2CL']
    
    newtf1 = int(MvarCL1)                           #Converting both accepted string numbers into integers
    newtf2 = int(MvarCL2)
    
    print newtf1
    print newtf2
    '''
    try:
        roboclaw.SpeedM1(address, newtf1)         #Slotting in the two motor integer values into roboclaw forward function
        roboclaw.SpeedM2(address, newtf2)
    except:
        print("problem with roboclaw")
        AttemptToConnectToRoboClaw()
        '''
      
#This webpage will be returned when the user presses submit button, the location.href function redirects the page back to rclaw_main.html so this is a placeholder page    
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
'''

#hosting the voice recognition website
@app.route('/VoiceRec')
def VoiceRec():
    return render_template('Google_SPEECH_API.html')


# hosting google map website (the root version i.e the first website which will show up when someone visits it)
@app.route('/RootMap')
def RootMap():
    #THIS SECTION FETCHES CURRENT GPS COORDINATES

    
    FinalStartLat = GetCurrentLatitude()
    FinalStartLong = GetCurrentLongitude()
    
    
    return render_template('maptest.html', LATpy=LATpy, LONGpy=LONGpy, FinalStartLong=FinalStartLong, FinalStartLat=FinalStartLat)


# The function whch will accept the location readings from the marker on the webpage
@app.route('/PRINTps/', methods=['POST','GET'])
def PRINTps():
    Var1=request.form['LAT']
    Var2=request.form['LONG']
    Var3 = request.form['KpLat']
    Var4 = request.form['KpLong']
    
    KpLatpy = float(Var3)
    KpLongpy = float(Var4)
    
    print ("Destination latitude is : " + Var1)
    print ("Destination longitude is : " + Var2)
    
    
    FinalStartLat = GetCurrentLatitude()
    FinalStartLong = GetCurrentLongitude()

    
    LATpy = Decimal(Var1)
    LONGpy = Decimal(Var2)
    
    MapMotion(FinalStartLat, FinalStartLong, LATpy, LONGpy, KpLatpy, KpLongpy )             #CALLING THE FUNCTION TO TRANSLATE THESE COORDINATES INTO MOTION
    
    return render_template('maptest.html', LATpy=LATpy, LONGpy=LONGpy, FinalStartLong=FinalStartLong, FinalStartLat=FinalStartLat)



#----------------Webpage button URL redirections, all the return statements are copy pasted and identical--------------------#
@app.route("/forward")
def forward():
    try:
        roboclaw.ForwardM1(address, 64)         #Custom forward motion tank motor values
        roboclaw.ForwardM2(address, 64)
    except:
        print("problem with roboclaw")
        AttemptToConnectToRoboClaw()   
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
'''
@app.route("/backward")
def backward():
    try:
        roboclaw.BackwardM1(address, 64)         #Custom backward motion tank motor values
        roboclaw.BackwardM2(address, 64)
    except:
        print("problem with roboclaw")
        AttemptToConnectToRoboClaw()   
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
'''

@app.route("/left")
def left():
    try:
        roboclaw.ForwardM1(address, 32)         #Custom left motion tank motor values
        roboclaw.ForwardM2(address, 64)
    except:
        print("problem with roboclaw")
        AttemptToConnectToRoboClaw()   
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
'''

@app.route("/right")
def right():
    try:
        roboclaw.ForwardM1(address, 64)         #Custom right motion tank motor values
        roboclaw.ForwardM2(address, 32)
    except:
        print("problem with roboclaw")
        AttemptToConnectToRoboClaw()   
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
'''

@app.route("/stop")
def stop():
    try:
        roboclaw.ForwardM1(address, 0)         #Custom stop motion tank motor values
        roboclaw.ForwardM2(address, 0)
    except:
        print("problem with roboclaw")
        AttemptToConnectToRoboClaw()   
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
'''

#------------EXPERIMENTAL VOICE RECOGNITION CODE, PROCEED WITH CAUTION. To use this change the html file call inside function form to Google_SPEECH_API.html----------#
#-----------Be careful since this does not have any proximity arguments and the motor speed is continuous once set----------------------------------------------------#
@app.route('/Decipher/', methods=['POST'])
def Decipher():
    Var1 = request.form['q']                    #Accepting the value from the website
    print (Var1)
    new1 = str(Var1)
    
    if (new1 == "forward" or new1.startswith('fe') or new1.startswith('fo') or new1.startswith('fy') or new1.startswith('fu') or new1.startswith('fa')):   #Checking to see if the spoken word is forward or starts with fe/fo/fy/etc
        try:
            roboclaw.ForwardM1(address, 64)         #Custom forward motion tank motor values
            roboclaw.ForwardM2(address, 64)
        except:
            print("problem with roboclaw")
            AttemptToConnectToRoboClaw()
            
    elif (new1 == "backward" or new1.startswith('ba') or new1.startswith('bo') or new1.startswith('by') or new1.startswith('bu') or new1.startswith('be')):
        try:
            roboclaw.BackwardM1(address, 64)         #Custom backward motion tank motor values
            roboclaw.BackwardM2(address, 64)
        except:
            print("problem with roboclaw")
            AttemptToConnectToRoboClaw()
            
    elif (new1 == "right" or new1.startswith('ry') or new1.startswith('ri') or new1.startswith('re') or new1.startswith('bright') or new1.startswith('ro')):
        try:
            roboclaw.ForwardM1(address, 64)         #Custom right motion tank motor values
            roboclaw.ForwardM2(address, 32)
        except:
            print("problem with roboclaw")
            AttemptToConnectToRoboClaw()
            
    elif (new1 == "left" or new1.startswith('ly') or new1.startswith('la') or new1.startswith('lo') or new1.startswith('le') or new1.startswith('lu')):
        try:
            roboclaw.ForwardM1(address, 32)         #Custom left motion tank motor values
            roboclaw.ForwardM2(address, 64)
        except:
            print("problem with roboclaw")
            AttemptToConnectToRoboClaw()
    else:
        roboclaw.ForwardM1(address, 0)         #Any other spoken word if slips through will make motors stop
        roboclaw.ForwardM2(address, 0)
            
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000/VoiceRec"
   </script>
   </head>
   <body>
   <h1>WOLOLOLO</h1>
   </body>
</html>
'''

#COORDINATE TO BUGGY MOTION FUNCTION
#East and West mean right and left and north and south mean forward and backward on specific frames
#This means the print statemnts take north to be forward and any subsequent east, west print statements mean left or right in that frame
def MapMotion(value1, value2, value3, value4, value5, value6):          #value1 and 2 is starting lat/long while value3/4 is ending lat/long while value5 is KpLat and value6 is KpLong
    
    try:
        StartLat = Decimal(value1)     #This value will be obtained from GPS module and will be different each time this loop iterates
    except:
        StartLat = 0
        
    try:
        StartLong = Decimal(value2)
    except:
        StartLong = 0

    EndLat = Decimal(value3)
    EndLong = Decimal(value4)
    
    KpLat = value5
    KpLong = value6
    
    #--------------------SECTION TO LIMIT WEB PAGE KPLAT AND KPLONG TO between 0 and 2---------------------#
    if (KpLat>2):
        KpLat = 2
    elif (KpLat<0):
        KpLat = 1
    else:
        KpLat = value5
        
    if (KpLong>2):
        KpLong = 2
    elif (KpLong<0):
        KpLong = 1
    else:
        KpLong = value6
    #-----------------------------------------------------------------------------------------#

    CurrentAngle = round(FindCurrentBearing())
    print ("CURRENT ANGLE IS THIS MUCH DEGREES: " + str(CurrentAngle))
    
    DestinationAngle = round(CalculateDestAngle(StartLat,StartLong,EndLat,EndLong))
    print ("DESTINATION ANGLE IS THIS MUCH DEGREES: " + str(DestinationAngle))
    
    FinalDistance = CalculateDestDistance(StartLong, StartLat, EndLong, EndLat)
    print("DISTANCE TO TRAVEL IN M IS: " + str(FinalDistance))
    
    #THIS WILL ROTATE THE TANK ABOUT ITS POINT UNTIL IT FACES THE DESTINATION
    while (CurrentAngle>(DestinationAngle+5) and CurrentAngle<(DestinationAngle-5)):
        roboclaw.ForwardM1(address, 70)         
        roboclaw.BackwardM2(address, 70)
        
        time.sleep(1)
        
    #TELL THE MOTORS TO GO SPECIFIC DISTANCE
    roboclaw.SpeedAccelDeccelPositionM1(address,120000,100000,120000,FinalDistance,0) #accel,spd,dec,pos
    roboclaw.SpeedAccelDeccelPositionM2(address,120000,100000,120000,FinalDistance,0) #accel,spd,dec,pos
        
    
    

#THIS FUNCTION WHEN CALLED WILL FETCH CURRENT TANK GPS LATITUDE
def GetCurrentLatitude():
    
    conn = db.connect('T8.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    ids1 = c.execute('SELECT Latitude FROM MonitorValues').fetchall()
    try:
        
        FinalStartLat = ids1[-1]
        return FinalStartLat
   
    except:
        print ('SOMETHING IS WRONG WITH YOUR GPS!!!!!!!!!!!!!!!!!CAUTION!!!!!!!!!!!!!!!')
        return (0)

#THIS FUNCTIoN WHEN CALLED WILL RETURN CURRENT TANK GPS LONGITUDE
def GetCurrentLongitude():
    
    conn = db.connect('T8.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    ids2 = c.execute('SELECT Longitude FROM MonitorValues').fetchall()
    try:
        
        FinalStartLong = ids2[-1]
        return FinalStartLong
   
    except:
        print ('SOMETHING IS WRONG WITH YOUR GPS!!!!!!!!!!!!!!!!!CAUTION!!!!!!!!!!!!!!!')
        return (0)
    
def CalculateDestAngle(SLat,SLong, ELat, ELong):

    lat1 = math.radians(SLat)
    lat2 = math.radians(ELat)

    diffLong = math.radians(ELong - SLong)

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)


    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing



def FindCurrentBearing():
    print ("INSERT STUFF TO DO WITH IMU TO FIND OUT WHAT CURRENT ORIENTATION IS")
    return 0
    

def CalculateDestDistance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


# Run the app :)
if __name__ == "__main__":

    #AttemptToConnectToRoboClaw()

    app.run(host='0.0.0.0', debug=True)
    
