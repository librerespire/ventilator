#!/usr/bin/env bash

nohup node index.js > /dev/null &
DISPLAY=:0 chromium-browser --app="http://localhost:8000" --start-fullscreen --force-device-scale-factor=1.50 > /dev/null 2> /dev/null &
echo "$(date) - Frontend started!!"
exit 0
