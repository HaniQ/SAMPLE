#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
from gps import *
from time import *
import time
import threading
import sqlite3 as lite
 
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  con = lite.connect('T8.db')
  name = "Ekram"
  
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      os.system('clear')
 
      print
      print ' GPS reading'
      print '----------------------------------------'
      ADAlat = gpsd.fix.latitude
      ADAlong = gpsd.fix.longitude
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      
      with con:
        
        cur = con.cursor()
        #cur.execute("DROP TABLE IF EXISTS MonitorValues")
        #cur.execute("CREATE TABLE MonitorValues(Latitude TEXT,Longitude TEXT, Name TEXT)")
        cur.execute("INSERT INTO MonitorValues (Latitude,Longitude,Name) VALUES(?,?,?)",(ADAlat,ADAlong,name))
        
        print ("SENT VALUES TO TABLE SUCCESSFULLY")
        
        print("READING VALUES FROM TABLE NOW..")

        con.row_factory = lambda cursor, row: row[0]

        ids1 = cur.execute('SELECT Latitude FROM MonitorValues').fetchall()
        ids2 = cur.execute('SELECT Longitude FROM MonitorValues').fetchall()
        
        FinalStartLat = ids1[-1]
        FinalStartLong = ids2[-1]
        
        print ("FINALSTARTLAT from table: "+ str(FinalStartLat))
        print ("FINALSTARTLONG from table: " + str(FinalStartLong))

 
      time.sleep(3) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
