#!/usr/bin/env bash

nohup node index.js > /dev/null &
DISPLAY=:0 chromium-browser --app="http://localhost:8000" --start-fullscreen > /dev/null &
echo "$(date) - Frontend started!!"
exit 0
