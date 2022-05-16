#!/bin/bash
date >> /home/pi/bleed-orange-measure-purple/update_log.txt
sudo echo "updating figures" >> log.txt
/home/pi/bleed-orange-measure-iaq/.venv/bin/python3 -E /home/pi/bleed-orange-measure-iaq/src/data/make_dashboard.py
