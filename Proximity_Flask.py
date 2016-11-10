#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

#Author: Ekram
#Using flask python web framework,javascript,html,css, some jquery,JSON and some ajax
#Basic understanding on the above required to understand code. Recommend going this route pythob->html->css->jscript->jquery->flask->sql->JSON and ajax
#Ajax is awesome in that it lets you load a specific variable from any function and edit it directly asyncronously into any webpage element, could not get
#it to work properly yet so omitted as of now. Must look into it to stop WHOLE page from having to refresh every 1 second
#After running this code the function index will host a webpage on the raspberry pi at http://localhost:5000, instead of localhost put pi IP address
#The webpage hosted is configured to refresh automatically every 1 second. And so every 1 second the proximity function is called and checks the distance
#The proximity distance is also sent to an sqlite database so that other concurrent programs can access it and work upon that argument 

from flask import Flask, render_template, request, url_for
import time
import RPi.GPIO as GPIO
# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def index():
    PDISTANCE = Proximity()
    
    #SQLITE SECTION. BASICALLY SENDING PROXIMITY READINGS INTO A TABLE DATABASE TO BE USED IN OTHER PROGRAMS AS MOTOR ARGUMENT#
    con = lite.connect('T7.db')
    name = "Ekram"

    with con:
    
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS MonitorValues")
        cur.execute("CREATE TABLE MonitorValues(Proximity INT, Name TEXT)")
        cur.execute("INSERT INTO MonitorValues (Proximity,Name) VALUES(?,?)",(PDISTANCE,name))
     #SQLITE SECTION END-----------------------------------------------------------------------------------------------------#
        
    if (PDISTANCE>1):
        DBool = 1               #I will use this bit as the argument to load red led image or safe led image on the website
    else:
        DBool = 0
    Monitor_Variables = {      # Storing variables as JSON to allow it to pass between javascript and python [note that str means string so all variables must be converted to string first]                         
                        'Distance': str(PDISTANCE),
                        'Bool'    : str(DBool)
                        }  
    
    #---------------------THIS WHOLE THING WILL BE LOADED INTO THE BROWSER OF WHOEVER GOES TO THE address localhost:5000, can use templates instead which makes for nicer looking code---------#
    return '''
<html>
  <head>
    <meta http-equiv="refresh" content="1" >
    <title>Home Page</title>
  </head>
  <body>
    <h1 style="height:100px; width:1900px">Obstacle in front of you is appx ''' + Monitor_Variables['Distance'] + ''' cm away </h1>
    
    <img id="I1" src="http://i.imgur.com/13jKyby.png">
    
    <script>
    function Get_Var(){
        Arg1 = ''' + Monitor_Variables['Bool'] + ''' ;
        return Arg1;
    };
    
    if (Get_Var() == 1)  {
    document.getElementById("I1").src = "http://i.imgur.com/b2Ir1DX.png";
}
    else {
     document.getElementById("I1").src = "http://i.imgur.com/98zj8Lu.png";  
    }
    </script>
  </body>
</html> '''

#---------------------Cannot comment on the above since whole thing is a string. Consult hand written notes to understand and remember what they do---------#
#---------------------Key thing to note is Monitor_variables which through JSON allows jscript and python to intermingle------------------------------------#

#The Ultra sound sensor function which will be called into the index function above every 1 second due to the webpage auto refreshing every 1 second
def Proximity():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    TRIG = 23                   #Proximity sensor pins
    ECHO = 24
    
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    
    GPIO.output(TRIG, False)
    
    GPIO.output(TRIG, True)
    
    time.sleep(0.00001)
    
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:

        pulse_start = time.time()
    
    while GPIO.input(ECHO)==1:

        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration*1750
    distance = round(distance, 2)
    print ("Distance:",distance,"cm")
    return distance


#This will effectively host the page        
if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0')
