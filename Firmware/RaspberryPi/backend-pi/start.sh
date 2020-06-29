##!/usr/bin/env bash
killall python3
python3 Controller.py > logs/debug.log 2> logs/error.log
