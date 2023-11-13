# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import  requests
import  os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
smtpserver = 'smtp.gmail.com'
smtpport = 587

server = smtplib.SMTP(smtpserver, smtpport)
server.starttls()
server.login(os.environ["GMAIL"], os.environ["GMAILPASS"])

text = 'Risyu_Stoped!!!!!!!!!!'
msg = MIMEText(text)
msg['Subject'] = 'Risyu_Stoped!!!!!!!!!!'
msg['From'] = os.environ["GMAIL"]
msg['To'] = os.environ["GMAIL"]
msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')


try:
    while True:
        with open('watchtest.txt', 'r', encoding='utf-8') as f:
            watchtest = f.read()
        print(watchtest)

        time.sleep(1)

except:
    #server.send_message(msg)
    #server.close()
    print('error')