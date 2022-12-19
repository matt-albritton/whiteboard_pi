#!/bin/bash
inkscape --select=Date --export-type=svg --export-filename="/home/mattspi/Downloads/whiteboard_pi/svgCreation/temp.svg" --actions="object-to-path;export-do;" ~/Downloads/whiteboard_pi/svgCreation/dashboard.svg
inkscape --select=Date --export-type=svg --export-filename="/home/mattspi/Downloads/whiteboard_pi/svgCreation/temp.svg" --actions="path-simplify;export-do;" ~/Downloads/whiteboard_pi/svgCreation/temp.svg
inkscape --export-filename=- ~/Downloads/whiteboard_pi/svgCreation/temp.svg | python hershey.py --output hershied.svg
