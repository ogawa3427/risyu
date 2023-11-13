import requests
import  os
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
smtpserver = 'smtp.gmail.com'
smtpport = 587

server = smtplib.SMTP(smtpserver, smtpport)
server.starttls()
server.login(os.environ["GMAIL"], os.environ["GMAILPASS"])

text = '📡📡📡📡📡RECIEVER_NOT_WORKS!!!!!!!!!!'
msg = MIMEText(text)
msg['Subject'] = '📡📡📡📡📡RECIEVER_error!!!!!!!!!!'
msg['From'] = os.environ["GMAIL"]
msg['To'] = os.environ["GMAIL"]
msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

while True:
    try:
# APIのURL
        url = 'http://20.78.138.195:5000/api'

# APIリクエストを送信
        response = requests.get(url)

        with open('recieved.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        
        time.sleep(49)
    except:
        server.send_message(msg)
        server.close()

        time.sleep(49)
# 変数の内容を表示（オプション）
    naiyou = response.json()
    print(naiyou[asof])
