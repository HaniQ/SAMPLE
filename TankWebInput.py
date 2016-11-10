#Importing all the relevant stuff
import time
import sys
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, url_for
from decimal import *

# Initialize the Flask application
app = Flask(__name__)

LATpy = 0
LONGpy = 0

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
    
    try:
        roboclaw.ForwardM1(address, int(Round(Actual_M1)))         #Slotting in the two motor integer values into roboclaw forward function
        roboclaw.ForwardM2(address, int(Round(Actual_M2)))
    except:
        print("problem with roboclaw")
        AttemptToConnectToRoboClaw()
#This webpage will be returned when the user presses submit button, the location.href function redirects the page back to rclaw_main.html so this is a placeholder page    
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.43.244:5000"
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
    return render_template('maptest.html', LATpy=LATpy, LONGpy=LONGpy)

# The function whch will accept the location readings from the marker on the webpage
@app.route('/PRINTps/', methods=['POST','GET'])
def PRINTps():
    Var1=request.form['LAT']
    Var2=request.form['LONG']
    
    print ("Destination latitude is : " + Var1)
    print ("Destination longitude is : " + Var2)
    
    LATpy = Decimal(Var1)
    LONGpy = Decimal(Var2)
    
    return render_template('maptest.html', LATpy=LATpy, LONGpy=LONGpy)



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
    window.location.href = "http://192.168.43.244:5000"
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
    window.location.href = "http://192.168.43.244:5000"
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
    window.location.href = "http://192.168.43.244:5000"
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
    window.location.href = "http://192.168.43.244:5000"
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
    window.location.href = "http://192.168.43.244:5000"
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
    window.location.href = "http://192.168.43.244:5000"
   </script>
   </head>
   <body>
   <h1>WOLOLOLO</h1>
   </body>
</html>
'''


# Run the app :)
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
