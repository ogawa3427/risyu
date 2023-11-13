import os
import re
import json
import paramiko
from scp import SCPClient
csvs_directory = os.path.join(os.path.expanduser('~'), 'risyu', 'csvs')
import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
smtpserver = 'smtp.gmail.com'
smtpport = 587

server = smtplib.SMTP(smtpserver, smtpport)
server.starttls()
server.login(os.environ["GMAIL"], os.environ["GMAILPASS"])

text = '📘📘📘📘📘SCP_ERROR!!!!!!!!!!'
msg = MIMEText(text)
msg['Subject'] = '📘📘📘📘📘SCPERROR!!!!!!!!!!'
msg['From'] = os.environ["GMAIL"]
msg['To'] = os.environ["GMAIL"]
msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

with open('kari.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

remote_host = json_data['remote_host']
remote_user = json_data['remote_user']
private_key_path = json_data['private_key_path']
remote_path = json_data['remote_path']

while True:
    try:
        
    # 'csvs'ディレクトリ内のファイルとディレクトリのリストを取得
        ls = os.listdir(csvs_directory)
        ls = [ls for ls in ls if re.search("risyu", ls)]
        ls = [ls for ls in ls if re.search("csv", ls)]

        numlist = [re.findall(r'\d+', fname)[0] for fname in ls if re.findall(r'\d+', fname)]
        openfile = max(numlist)
        openfile = re.sub(r'^', 'risyu', openfile)
        openfile = re.sub(r'$', '.csv', openfile)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_host, username=remote_user, key_filename=private_key_path)

        with SCPClient(ssh.get_transport()) as scp:
            scp.put(os.path.join(csvs_directory, openfile), remote_path=remote_path)

        ssh.close()

        print('CSV_sent_sucsessfuly')
        print(openfile)

        time.sleep(49)
    
    except:
        print('CSV_send_error')
        print(openfile)
        server.connect(smtpserver, smtpport)
        server.send_message(msg)
        server.close()

        time.sleep(49)


                    


