# SAMPLE
Team SAMPLE's collection of code for the project 

List of what the different files do:

AutoMov.py   ---> This contains unfinished code which will translate map co-ordinates into movement of the buggy. Alo contains automatic spiral rectangle motion of buggy

Google_SPEECH_API.html    ----> This is the html code displayed to the user on the browser. This will accept voice commands and relay it back to the raspberry pi where it can decide what to do with it. For now it is running the roboclaw based on specific voice commands.

Map_GPS.py     ----> This hosts a google map web page on which the tank position can be seen. It can also accept co-ordinates input by the user on the browser

Proximity_Flask.py   ------> A demo code which hosts a web page on which proximity readings are streamed in real time with actual analog values.

Rclaw_Flask.py   ------> The main web based manual control backend code for the buggy. This hosts the page which contains the dbutton images to control the buggy

Rclaw_main.html   ----> The web page containing the dbuttons / text fields displayed to the user during manual control

TankWebInput.py  -----> A mega python code which integrates all of the above into a single code

index.html  -----> the home page shown to the user on the browser containing information about the project

maptest.html -----> The google map web page hosted by Map_GPS.py
