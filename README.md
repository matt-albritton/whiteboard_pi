# The RoboBoard
A repo for my CS490 thesis project "robotic whiteboad".

Final Writeup:
https://drive.google.com/file/d/1fR7KXrv4AAl0u252UBi9K_cug9v1NrdN/view?usp=sharing

Videos:
Time-Lapse
https://www.youtube.com/watch?v=O2icEaGkBxk
[![RoboBoard Time-Lapse](https://img.youtube.com/vi/O2icEaGkBxk/0.jpg)](https://www.youtube.com/watch?v=O2icEaGkBxk)

Start-Up
https://www.youtube.com/watch?v=GFNDBqp8anI 
[![RoboBoard Time-Lapse](https://img.youtube.com/vi/GFNDBqp8anI/0.jpg)](https://www.youtube.com/watch?v=GFNDBqp8anI)

Images:
Base Format: 
![image](https://user-images.githubusercontent.com/60043682/208540982-f3204b28-4c8a-4b27-b619-90921aa3c8ee.png)

With API data input:
![image](https://user-images.githubusercontent.com/60043682/208544381-79d9e868-22fb-40a2-bb80-36d15b3f13d9.png)

Text -> Hershey Text: 
![image](https://user-images.githubusercontent.com/60043682/208542482-05af0eb9-95b6-44f0-bac0-64b23e23e87b.png)

On Whiteboard: 
![IMG_4959](https://user-images.githubusercontent.com/60043682/208542254-e3e2f325-6ddf-4a7b-bdfa-88f5fbf9f31e.jpg)

Project Abstract:
	To fulfill my computer science major senior requirement, I designed and built a small robotic whiteboard. The purpose of this build is to fuse the artistic intrigue of robotic-drawing, and the usefulness of a daily dashboard. This device connects to the internet, pulls useful daily information, and draws that information out on the whiteboard autonomously each morning. It is currently configured to display the weather, the previous day’s sports scores, my calendar for the day, and an inspirational quote. The concept came from a desire to explore the interface between machines and art and the concept of a robot doing the inherently human task of writing with a marker. I decided a morning briefing would be a very useful and fun way of putting the machine to use. The drawing mechanism is built on a small whiteboard and utilizes a hanging-v design where two stepper motors control the marker hanging between them. This is driven by an Arduino hooked to a Raspberry Pi to perform the image creation and control. The code base is built on a pre-existing repository for the control of drawing machines. The bulk of my work built upon this, fine tuning to my build and automating the data collection, image creation, and drawing initiation processes. I wrote a combination of Python and Bash scripts to automate the data gathering process and utilized Inkscape for SVG file creation and editing. I then passed those to a Processing script which interfaced with the Arduino to control the robot. The final product is a completely autonomous system that is practical to the user, visually engaging, and technologically captivating. 

This project is heavily based upon the Polargraph project by Sandy Noble 2015.
Found here: https://github.com/euphy/polargraphcontroller/tree/2017-11-01-20-30

This repo holds all necessary added functionality of the rasberry pi - so acts as a form of back up as well.
It holds the two main code bases, the pi and the arduino.


================= Running The Project ================
In the top level directory, this project can be ran simply by calling "python always_on.py". 
This small python file will run, and whenever it is 6am, will call the bash script "run.sh"
This first runs the python file "combination_api_svg.py" which calls all necessary apis. Then, using "dash_og.svg" it fills in all the information into the proper 
locations in the svg file. That is saved to "dashboard.svg" 
Next run.sh calls an inkscape action to transform the date text into a path- getting the block letters and simplifies the nodes. This is saved in temp.svg
Then it converts the rest of the text into hershey text, using "hershey.py" (an inkscape extension) This is saved in hershed.svg
Lastly run.sh runs the processing script "polargraphcontroller" which is set to import hershed.svg automatically and begin transmiting to the arduino to draw. 
The processing window is killed after 5 hours when the drawing is complete, but "always_on.py" continues to run.

