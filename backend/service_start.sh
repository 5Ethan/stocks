#!/bin/bash

pip install -r requirements.txt

nohup python main.py > stocks-backend.log 2>&1 &

