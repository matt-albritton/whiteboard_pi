#!/bin/bash
# cd svgCreation
# python combination_api_svg.py
# sh do_hershey.sh
# cd ..
timeout --foreground 1m DISPLAY=:0 /home/mattspi/Downloads/whiteboard_pi/processing-2.2.1/processing-java --sketch=/home/mattspi/Downloads/whiteboard_pi/polargraphcontroller --output=/home/mattspi/Downloads/whiteboard_pi/processing-2.2.1/output --force --run
