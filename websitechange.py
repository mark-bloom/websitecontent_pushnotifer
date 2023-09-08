## Check Twice ticket availability
## Notification by selection
# A = computer only
# B = mobile only
# other or no input = both

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from pushnotifier.exceptions import *
from selenium.webdriver.firefox.options import Options

from datetime import datetime

from pushnotifier import PushNotifier as pn
username = "" # insert pushnotifer account username
password = "" # insert pushnotifer account password
api_key = "" # insert pushnotifer API key
package_name = "com.generic.app" # insert pushnotifer app package name

import sys # for reading in arguments
import time
import re

## CUSTOMISE WEBSITE TO CHECK
urlweb = "" # what website you will check
sitename = "" # give notification title

devicesweb = [""] # pusnotifer device, must be in array

# Notify via desktop beep
# Notify via push notification or by desktop beep
def notifyme(msg, timenow):
    if(len(sys.argv) == 2):
        if(sys.argv[1] == "A"):
            print('\007', end='\r')
            time.sleep(1)
            print('\007', end='\r')
        elif(sys.argv[1] == "B"):
            msg_result = pn.send_notification(msg + " : " + timenow, urlweb, devicesweb)
        else: # any single character argument not A or B
            print('\007', end='\r')
            time.sleep(1)
            print('\007', end='\r')
            msg_result = pn.send_notification(msg + " : " + timenow, urlweb, devicesweb)
    else: # not a single character as argument
        print('\007', end='\r')
        time.sleep(1)
        print('\007', end='\r')
        msg_result = pn.send_notification(msg + " : " + timenow, urlweb, devicesweb)

def init_pushnotifier(pnX):
    try:
        pn = pnX.PushNotifier(username, password, package_name, api_key)
        return pn
    except IncorrectCredentialsError:
        print(username + ": Incorrect credentials!")
    except UserNotFoundError:
        print(username + ": User not found!")

# Firefox options
options = Options()
options.add_argument("--headless")

# Initialise pushnotifier
pn = init_pushnotifier(pn)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

delay = 30 # maximum time in seconds for page load
sleep_time = 1800 # time between cycles
loading_time = 100 # time between 'too long to load'

# Initialise browser
browser = webdriver.Firefox(options=options)
while(True):
    try:
        browser.get(urlweb)
        time.sleep(5)
        browser.refresh()
        break
    except WebDriverException:
        time.sleep(loading_time)
        
# First run
while(True):
    try:
        body = browser.find_element(By.TAG_NAME, "body")
        original = body.text

        print("Page is ready:")
        time.sleep(sleep_time)
        break
    except TimeoutException:
        print("Loading took too much time! " + current_time + "            ")
        time.sleep(loading_time)

# Checking for changes
count = 0
while(True):
    while(True):
        try:
            browser.refresh()
            break
        except WebDriverException:
            time.sleep(loading_time)
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    count += 1
    
    try:
        body = browser.find_element(By.TAG_NAME, "body")
        new = body.text
        if(new == original):
            print("No change - Refreshed " + str(count) + " times.", end='\r')
        else:   
            notifyme(sitename,current_time)
            print(sitename,"WEBSITE CHANGED!                    ")
            time.sleep(sleep_time)
            exit()
    except TimeoutException:
        print("Loading took too much time! " + current_time + "            ")
        time.sleep(loading_time)
    time.sleep(sleep_time)
