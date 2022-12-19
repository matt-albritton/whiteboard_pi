#!/bin/bash
cd svgCreation
python combination_api_svg.py
#doing hershey changes
inkscape --select=Date --export-type=svg --export-filename="/home/mattspi/Downloads/whiteboard_pi/svgCreation/temp.svg" --actions="object-to-path;export-do;" ~/Downloads/whiteboard_pi/svgCreation/dashboard.svg
inkscape --select=Date --export-type=svg --export-filename="/home/mattspi/Downloads/whiteboard_pi/svgCreation/temp.svg" --actions="path-simplify;export-do;" ~/Downloads/whiteboard_pi/svgCreation/temp.svg
inkscape --export-filename=- ~/Downloads/whiteboard_pi/svgCreation/temp.svg | python hershey.py --output hershied.svg
cd ..
{
    sleep 5h
    pkill processing-java
    pkill java
} &
DISPLAY=:0 /home/mattspi/Downloads/whiteboard_pi/processing-2.2.1/processing-java --sketch=/home/mattspi/Downloads/whiteboard_pi/polargraphcontroller --output=/home/mattspi/Downloads/whiteboard_pi/processing-2.2.1/output --force --run &
