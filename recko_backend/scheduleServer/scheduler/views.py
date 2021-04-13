from django.shortcuts import render

# Create your views here.
import schedule
import time
import datetime
import json
import requests
from urllib.request import urlopen
import schedule
import io
import sys
import time
import pickle
import os
import json
from datetime import date

########################## PUT THIS ON A DIFFERENT DJANGO SERVER AND RUN IT DAILY ######################

##################### SET SCHEDULE TIME TO 86400 seconds IN schedule.every() ###########################

def wait_for_internet_connection():
  while True:
      try:
          response = urlopen('https://www.google.com/', timeout = 1)
          return
      except Exception as e:
          pass


def job():
    #print("AA")
    response1=requests.get("http://127.0.0.1:8000/qbo",timeout=5)
    response2=requests.get("http://127.0.0.1:8000/xeroData",timeout=5)
    #fetch data by call quickbooks api and xero api
    #print(response1.text.encode('utf8'),"\n\n\n\n",response2.text.encode('utf8'))

# Run job every 3 second/minute/hour/day/week,
# Starting 3 second/minute/hour/day/week from now
schedule.every(86400).seconds.do(job)


while True:
    wait_for_internet_connection()
    schedule.run_pending()
    time.sleep(1) 
