#!/bin/bash
apt-get update
apt-get dist-upgrade

roscore &
cd WHF/catkin_ws/src/beginner_tutorials/scripts/

TERM_PID=$(echo `ps -C gnome-terminal -o pid= | head -1`) # get first gnome-terminal's PID
WID=$(wmctrl -lp | awk -v pid=$TERM_PID '$3==pid{print $1;exit;}') # get window id

xdotool windowfocus $WID
xdotool key ctrl+shift+t # my key map
xdotool sleep $DELAY # it may take a while to start new shell :(
xdotool type --delay 1 --clearmodifiers "$@"
xdotool key Return
roslaunch uol_turtlebot_simulator object-search-training.launch

wmctrl -i -a $WID # go to that window (WID is numeric)


