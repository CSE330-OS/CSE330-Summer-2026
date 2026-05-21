#!/bin/bash
#
sudo apt-get install -y ffmpeg libsm6 libxext6
sudo apt-get install -y tesseract-ocr
sudo apt install python3
sudo apt install python3-pip

sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
