#Author: Ekram
'''
This code is supposed to run cocurrently with main code TankWebInput.py. This basically sets up a websocket and accepts 
gps coords from my android phone. Run this by ssh ing two windows with this in 1 and TankWebInput.py in the other
'''


#server script
import socket
import time
import sqlite3 as lite

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("192.168.43.244",12345))
sock.listen(2)
(client,(ip,port))=sock.accept()


con = lite.connect('T8.db')
name = "Ekram"

while True:
    gpsdata = client.recv(1204)
    locString = str(gpsdata)
    SlicedString = locString[70:161]
    print (SlicedString)
        
        
    with con:
        
        cur = con.cursor()
        #cur.execute("DROP TABLE IF EXISTS MonitorValues")
        #cur.execute("CREATE TABLE MonitorValues(GPS TEXT, Name TEXT)")
        cur.execute("INSERT INTO MonitorValues (GPS,Name) VALUES(?,?)",(SlicedString,name))
            
    time.sleep(3)

