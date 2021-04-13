import schedule
import time
import datetime
import json
import requests

########################## PUT THIS ON A DIFFERENT DJANGO SERVER AND RUN IT DAILY ######################

##################### SET SCHEDULE TIME TO 86400 seconds IN schedule.every() ###########################

def job():
    response1=requests.get("http://localhost:8000/qbo")
    response2=requests.get("http://localhost:8000/xeroData")
    #fetch data by call quickbooks api to fetch data
    print(response1.text.encode('utf8'),"\n\n\n\n",response2.text.encode('utf8'))

# Run job every 3 second/minute/hour/day/week,
# Starting 3 second/minute/hour/day/week from now
schedule.every(3).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1) 
