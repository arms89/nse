#!/bin/bash

echo 
echo ----------------------------------------------------------------
cd /home/ubuntu/nse_signals/
echo Data Sync Started
/home/ubuntu/miniconda3/bin/python3  /home/ubuntu/nse_signals/main.py
echo Data Sync Ended
echo ----------------------------------------------------------------
echo Git Commit started
d=$(date +%d-%m-%Y)
echo $(pwd)
/usr/bin/git add .
/usr/bin/git add -u
/usr/bin/git commit -m "$d"
/usr/bin/git push origin master
echo git commit ended
echo ----------------------------------------------------------------
exit
