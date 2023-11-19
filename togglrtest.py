import json
import time

toggle = 0
scptname = '01seleniumer'

while True:
    with open('deadoralive.json', 'r', encoding='utf-8') as f:
        deadoralive = json.load(f)
    
    deadoralive[scptname][scptname + str(toggle)] = int(time.time()/1)

    diff01 = abs(deadoralive[scptname][scptname + '0'] - deadoralive[scptname][scptname + '1'])
    deadoralive[scptname][scptname + '_diff'] = diff01

    with open('deadoralive.json', 'w', encoding='utf-8') as f:
        json.dump(deadoralive, f, indent=4)

    toggle = 1 - toggle


    time.sleep(10)