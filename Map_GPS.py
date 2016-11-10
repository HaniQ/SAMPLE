
from flask import Flask, render_template, request, url_for
import RPi.GPIO as GPIO
import time
from decimal import *



# Initialize the Flask application
app = Flask(__name__)

LATpy = 0
LONGpy = 0


# Define a route for the default URL, which loads the form
@app.route('/')
def index():
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




#This will host the page        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
