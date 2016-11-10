#Author: Ekram
#Made 30/10/2016
#Roboclaw stuff was copy pasted from Sam's code
#Using python web flask framework, html and javascript and a little jquery
#THIS DOES NOT HAVE PROXIMITY SENSING YET SO PROCEED WITH CAUTION
#WORK LEFT: Adding sqlite to fetch proximity readings from the Monitor_values table in t7.db and use that as argument to limit motion of the tank
#VERY IMPORTANT: BEFORE RUNNING THIS MAKE SURE ALL THE ROOT WEBPAGE ADDRESS IN THIS CODE MATCHES WITH THE pi's IP ADDRESS
#Place Rclaw_Flask.py inside /home/pi AND create a folder inside /home/pi called templates and place Rclaw_main.html in there
#Run Rclaw_Flask.py from linux command terminal to run this program
#To activate the voice rec stuff add Google_Speech_API.html in the templates folder and edit it in on line 44 instead of Rclaw_main.html

#Importing all the relevant stuff
import time
import sys
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, url_for

#Setup MQTT connection to send values from pad
mqttc=mqtt.Client()
mqttc.username_pw_set('sam','mosquitto1894')
mqttc.connect("130.88.154.7",1894,60)                 #"localhost:1883" or "10.42.0.1:1883"
mqttc.loop_start() #start threaded so the pygame stuff can work


# Initialize the Flask application
app = Flask(__name__)

      
        
# Define a route for the default URL, which loads the form. This is root so this webpage will be output to whoever goes to address http://localhost:5000 (localhost= pi IP address)
@app.route('/')
def form():
    return render_template('Rclaw_main.html')


# Define a route for the action of the form, for example '/ManualF/' NOTE THAT THIS IS ONLY FOR FORWARD MOVEMENT, FOR BACKWARD COPY PASTE THIS WITH FORWARD CHANGED TO BACKWARD
@app.route('/ManualF/', methods=['POST'])
def Manual():
    Mvar1=request.form['Motor1']                #Accepting both motor value input from the web page as a string
    Mvar2=request.form['Motor2']
    
    new1 = int(Mvar1)                           #Converting both accepted string numbers into integers, they are still percentage tho
    new2 = int(Mvar2)
    
    Actual_M1 = (new1/100)*127                  #Converting % into actual values from 0 to 127 scale
    Actual_M2 = (new2/100)*127
    
    try:
        mqttc.publish("RoboClaw/MotorOne/PWM", str(Actual_M1), 0)
        mqttc.publish("RoboClaw/MotorTwo/PWM", str(Actual_M2), 0)
    except:
        print("ERROR COULD NOT PUBLISH VALUES")
        
#This webpage will be returned when the user presses submit button, the location.href function redirects the page back to rclaw_main.html so this is a placeholder page    
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.137.214:5000"
   </script>
   </head>

   <body>
   <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either your internet connection in hiccuping or somethng  else went horribly wrong</h1>
   </body>
</html>
'''

#-------------------THIS SECTION IS FOR THE BROWSER DIRECTIONAL BUTTONS TO CONTROL THE TANK----------------------------------#
#----------------Webpage button URL redirections, all the return statements are copy pasted and identical--------------------#
@app.route("/forward")
def forward():
    try:
        mqttc.publish("RoboClaw/MotorOne/PWM",'32', 0)
        mqttc.publish("RoboClaw/MotorTwo/PWM",'32', 0)
    except:
        print("ERROR COULD NOT PUBLISH")
    
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.137.214:5000"
   </script>
   </head>

   <body>
      <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either your internet connection in hiccuping or somethng  else went horribly wrong</h1>
   </body>
</html>
'''
@app.route("/backward")
def backward():
    try:
        mqttc.publish("RoboClaw/MotorOne/PWM",'-32', 0)
        mqttc.publish("RoboClaw/MotorTwo/PWM",'-32', 0)
    except:
        print("ERROR COULD NOT PUBLISH")
 
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.137.214:5000"
   </script>
   </head>

   <body>
     <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either your internet connection in hiccuping or somethng  else went horribly wrong</h1>
   </body>
</html>
'''

@app.route("/left")
def left():
    try:
        mqttc.publish("RoboClaw/MotorOne/PWM",'64', 0)
        mqttc.publish("RoboClaw/MotorTwo/PWM",'32', 0)
    except:
        print("ERROR COULD NOT PUBLISH")

    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.137.214:5000"
   </script>
   </head>

   <body>
    <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either your internet connection in hiccuping or somethng  else went horribly wrong</h1>
   </body>
</html>
'''

@app.route("/right")
def right():
    try:
        mqttc.publish("RoboClaw/MotorOne/PWM",'32', 0)
        mqttc.publish("RoboClaw/MotorTwo/PWM",'64', 0)
    except:
        print("ERROR COULD NOT PUBLISH")

    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.137.214:5000"
   </script>
   </head>

   <body>
     <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either your internet connection in hiccuping or somethng  else went horribly wrong</h1>
   </body>
</html>
'''

@app.route("/stop")
def stop():
    try:
        mqttc.publish("RoboClaw/MotorOne/PWM",'0', 0)
        mqttc.publish("RoboClaw/MotorTwo/PWM",'0', 0)
    except:
        print("ERROR COULD NOT PUBLISH")
        
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.137.214:5000"
   </script>
   </head>

   <body>
     <h1>The script above me is supposed to redirect this page back to rclaw_main.html before I finish loading.
   If you can read this, either your internet connection in hiccuping or somethng  else went horribly wrong</h1>
   </body>
</html>
'''
#------------------------BROWSER DIRECTIONAL BUTTONS URL REDIRECTIONS END---------------------------------------------------------------------------------#


#-------THIS IS EXPERIMENTAl VOICE RECOGNITION TANK CONTROL, PROCEED WITH CAUTION, THIS IS TO BE RUN ON TOP OF GOOGLE WEB SPEECH DICTATION KIT-------------#
#Current commands: LEFT,RIGHT,FORWARD,BACKWARD and INITIALISE. (Anything not recognized will stop the motors)
#Commands to add: STATUS(Open a new browser tab with monitor values) , POSITION(Open a new browser tab with position on google maps) 
@app.route('/Decipher/', methods=['POST'])
def Decipher():
    Var1 = request.form['q']
    print (Var1)
    print (Var1)
    print (Var1)
    new1 = str(Var1) #Var1 should already be a string but just to be sure, converting it again incase the microphone decides to record something as int
    
    if (new1 == "forward" or new1.startswith('fo') or new1.startswith('fa') ):   #This will return true if the spoken word is forward OR if the spoken word starts with fo/fa
        try:
            mqttc.publish("RoboClaw/MotorOne/PWM",'32', 0)
            mqttc.publish("RoboClaw/MotorTwo/PWM",'32', 0)
        except:
            print("ERROR COULD NOT PUBLISH")
            
    elif (new1 == "backward" or new1.startswith('ba') or new1.startswith('bu') ): #This will return true if the spoken word is backward OR if the spoken word starts with ba/bu
        try:
            mqttc.publish("RoboClaw/MotorOne/PWM",'-32', 0)
            mqttc.publish("RoboClaw/MotorTwo/PWM",'-32', 0)
        except:
            print("ERROR COULD NOT PUBLISH")
            
    elif (new1 == "left" or new1.startswith('le') or new1.startswith('lo') or new1.startswith('li') or new1.startswith('ly') ):  #This will return true if the spoken word is left OR if the spoken word starts with le/lo/ly
        try:
            mqttc.publish("RoboClaw/MotorOne/PWM",'64', 0)
            mqttc.publish("RoboClaw/MotorTwo/PWM",'32', 0)
        except:
            print("ERROR COULD NOT PUBLISH")

            
    elif (new1 == "right" or new1.startswith('ri') or new1.startswith('ry') or new1.startswith('bri') ):    #This will return true if the spoken word is right/bright OR if the spoken word starts with ri/ry
        try:
            mqttc.publish("RoboClaw/MotorOne/PWM",'32', 0)
            mqttc.publish("RoboClaw/MotorTwo/PWM",'64', 0)
        except:
            print("ERROR COULD NOT PUBLISH")
                
            
    else:
        mqttc.publish("RoboClaw/MotorOne/PWM",'0', 0)
        mqttc.publish("RoboClaw/MotorTwo/PWM",'0', 0)
    return '''
<!DOCTYPE html>
   <head>
      <title>Redirect</title>
      <script language="javascript">
    window.location.href = "http://192.168.137.214:5000"
   </script>
   </head>

   <body>
   <h1>WOLOLOLO</h1>
   </body>
</html>
'''
#----------------------EXPERIMENTAL VOICE RECOGNITION CODE END---------------------------------------------------------#


        

# Run the app :)
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)




