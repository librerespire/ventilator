#!/usr/bin/env bash

killall node chromium-browser
nohup node index.js > /dev/null &
sleep 10s
DISPLAY=:0 chromium-browser --app="http://localhost:8000" --start-fullscreen --force-device-scale-factor=0.93 > /dev/null 2> /dev/null &
echo "$(date) - Frontend started!!"
exit 0
