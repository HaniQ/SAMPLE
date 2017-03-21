  
'''
Author: Ekram
Made 30/10/2016
Using python web flask framework, html and javascript and jquery
THIS DOES NOT HAVE PROXIMITY SENSING YET SO PROCEED WITH CAUTION
WORK LEFT: Adding sqlite to fetch proximity readings from the Monitor_values table in t8.db and use that as argument to limit motion of the tank
VERY IMPORTANT: BEFORE RUNNING THIS MAKE SURE ALL THE ROOT WEBPAGE ADDRESS IN THIS CODE MATCHES WITH THE pi's IP ADDRESS
DO NOT tamper with the voice recognition stuff or go to the web page while code is running. It does not have any catch/motor limiters so might make buggy go haywire with stray voice commands
'''

#Importing all the relevant stuff
#from roboclaw import *
from flask import Flask, render_template, request
from decimal import *
import socket


#Global Vars
address = 0x80              #Roboclaw Address


# Initialize the Flask application
app = Flask(__name__)

LATpy = 0
LONGpy = 0


def ReturnOwnIpAddress():
    hostname = socket.gethostname()
    IP = socket.gethostbyname(hostname)

    return (str(IP))

IP_Address = ReturnOwnIpAddress()

#----Roboclaw connection function-----------#
def AttemptToConnectToRoboClaw():
    try:
        '''for windows use COM3'''
        roboclaw.Open("/dev/ttyACM0",115200)
        #Motor safe state
        roboclaw.ForwardMixed(address, 0)
        roboclaw.TurnRightMixed(address, 0)
       
    except Exception as e:
        print("problem with roboclaw")
       

# Define a route for root webpage. This is root so this webpage will be output to whoever goes to address http://localhost:5000 (localhost= pi IP address)
@app.route('/')
def index():
    return render_template('index.html', IP_Address=IP_Address)

#Root webpage to display manual buttons for the roboclaw
@app.route('/DBUTTONS')
def DBUTTONS():
    return render_template('Rclaw_main.html', IP_Address=IP_Address)

#NOTE manual readings as % for motors OPEN LOOP
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
    '''    
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
    '''            
#This webpage will be returned when the user presses submit button, the location.href function redirects the page back to rclaw_main.html so this is a placeholder page    
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://''' + IP_Address + ''':7000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
        '''

#NOTE manual readings as % for motors CLOSED LOOP
@app.route('/ManualCL/', methods=['POST'])
def ManualCL():
    MvarCL1=request.form['Motor1CL']                #Accepting both motor value input from the web page as a string
    MvarCL2=request.form['Motor2CL']
    
    newtf1 = int(MvarCL1)                           #Converting both accepted string numbers into integers
    newtf2 = int(MvarCL2)
    
    print (newtf1)
    print (newtf2)
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
    window.location.href = "http://''' + IP_Address + ''':7000/DBUTTONS"
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
    return render_template('Google_SPEECH_API.html', IP_Address=IP_Address)


# hosting google map website (the root version i.e the first website which will show up when someone visits it)
@app.route('/RootMap')
def RootMap():
    #THIS SECTION FETCHES CURRENT GPS COORDINATES
    FinalStartLong = -2.2344839572906499
    FinalStartLat = 53.47541458927213


    return render_template('maptest.html',LATpy=LATpy, LONGpy=LONGpy,FinalStartLong=FinalStartLong,FinalStartLat=FinalStartLat,IP_Address=IP_Address)


# The function whch will accept the location readings from the marker on the webpage
@app.route('/PRINTps/', methods=['POST','GET'])
def PRINTps():
    Var1=request.form['LAT']
    Var2=request.form['LONG']
    
    print ("Destination latitude is : " + Var1)
    print ("Destination longitude is : " + Var2)

    '''accept gps coord from sql table here. this will be finalstart long and lat'''
    FinalStartLong = 53.4616735
    FinalStartLat = -2.2303168
    
    LATpy = Decimal(Var1)
    LONGpy = Decimal(Var2)
    
      
    return render_template('maptest.html', LATpy=LATpy, LONGpy=LONGpy, FinalStartLong=FinalStartLong, FinalStartLat=FinalStartLat,IP_Address=IP_Address)

@app.route('/NDVI')
def NDVImap():
    '''this will showcase a map where ndvi values from text file will be taken and superimposed on map'''
   #THIS SECTION FETCHES CURRENT GPS COORDINATES
    FinalStartLong = -2.2344839572906499
    FinalStartLat = 53.47541458927213

    NDVI_COORD = []
    RGB_LIST = []

    with open('NDVI.txt') as f:
        content = f.readlines()

    content = [x.strip() for x in content] 

    count = 0
    while (count<(len(content)-1)):
        NDVI_COORD.append(content[count])
        next_i = count+1
        RGB_LIST.append(content[next_i])

        count = count+2

    '''Converting the list into a full string with : separators to pass into js page'''
    FullString_NDVI = ''
    for line in NDVI_COORD:
        FullString_NDVI+= line+':'

    FullString_RGB = ''
    for colorLine in RGB_LIST:
        FullString_RGB+= colorLine+':'

    return render_template('maptest.html',LATpy=LATpy, LONGpy=LONGpy,FinalStartLong=FinalStartLong,FinalStartLat=FinalStartLat,FullString_NDVI=FullString_NDVI,FullString_RGB=FullString_RGB, IP_Address=IP_Address)

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
    window.location.href = "http://''' + IP_Address + ''':7000/DBUTTONS"
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
    window.location.href = "http://''' + IP_Address + ''':7000/DBUTTONS"
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
    window.location.href = "http://''' + IP_Address + ''':7000/DBUTTONS"
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
    window.location.href = "http://''' + IP_Address + ''':7000/DBUTTONS"
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
    window.location.href = "http://''' + IP_Address + ''':7000/DBUTTONS"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
        '''

#------------EXPERIMENTAL VOICE RECOGNITION CODE, PROCEED WITH CAUTION. ----------------------------------------------------------------------------------------------#
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
    window.location.href = "http://''' + IP_Address + ''':7000/VoiceRec"
   </script>
   </head>
   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either you have slow internet or somethng went horribly wrong</h1>
   </body>
</html>
        '''





# Run the app :)
if __name__ == "__main__":

    #AttemptToConnectToRoboClaw()

    app.run(host=IP_Address,port=7000, debug=True)
