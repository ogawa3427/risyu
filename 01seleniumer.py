# coding: UTF-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import  requests
import  os
import  json
import re
import csv
import  bs4
import  sys
import  json

from datetime import datetime

target = 'https://eduweb.sta.kanazawa-u.ac.jp/portal/Public/Regist/RegistrationStatus.aspx?year=2024&lct_term_cd=22'
args = sys.argv
if len(args) > 1 and args[1] == 'test':
    target = 'https://ogawa3427.github.io/risyu-error_page/dummy.html'
else:
    target = 'https://eduweb.sta.kanazawa-u.ac.jp/portal/Public/Regist/RegistrationStatus.aspx?year=2024&lct_term_cd=22'

toggle = 0
scptname = '01seleniumer'

while True:
    try:
        options = Options()
        options.add_argument("--headless")
        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=options)

        driver.get(target)
        driver.implicitly_wait(5)
        driver.save_screenshot("screenshot.png")

        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_phContents_ucRegistrationStatus_ddlLns_ddl"))
        )
        select = Select(select_element)
        select.select_by_value('0')

        driver.implicitly_wait(5)
        driver.save_screenshot("screenshot2.png")

        page_source = driver.page_source
        with open("raw.html", "w", encoding="utf-8") as file:
            file.write(page_source) 

        driver.quit()

        print('success')

        csvs_directory = os.path.join(os.getcwd(), 'rcsvs')

        with open('raw.html', 'r', encoding='utf-8') as file:
            page_source = file.read()

        bs = bs4.BeautifulSoup(page_source, 'html.parser')

        # 指定されたtableを取得するためのコード
        table = bs.find('table', {'id': 'ctl00_phContents_ucRegistrationStatus_gv'})

        date = bs.find('span', {'id': 'ctl00_phContents_ucRegistrationStatus_lblDate'}).text
        meta_data = [
            date
        ]
        if len(args) > 1 and args[1] == 'test':
            meta_data.append('test')
        else:
            meta_data.append('valid')

        with open('output.tsv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            writer.writerow(meta_data)
            
            # ヘッダーを動的に取得して書き出す
            header_row = table.find('tr')
            headers = [header.text.strip() for header in header_row.find_all('th')]
            writer.writerow(headers)

            # 各行について情報を抽出し、TSVに書き出す
            for row in table.find_all('tr')[1:]:  # 最初の行はヘッダーなのでスキップ
                cols = row.find_all('td')
                if cols:
                    data = []
                    for col in cols:
                        # <span>タグがあれば、そのテキストを取得
                        span = col.find('span')
                        if span:
                            data.append(span.text.strip().replace('\n', ' '))
                        else:
                            # <td>タグ内のテキストから改行をスペースに置換
                            data.append(col.text.strip().replace('\n', ' '))
                    writer.writerow(data)

        print('success2 written output.tsv')
        with open('output.tsv', 'r', encoding='utf-8') as f:
            tsv = f.read()
        tsv = tsv.split('\n')
        for i in range(len(tsv)):
            tsv[i] = tsv[i].split('\t')

        datetime_obj = datetime.strptime(tsv[0][0], '%Y/%m/%d %H:%M:%S')
        # print(datetime_obj)
        date_str = datetime_obj.strftime('%Y%m%d%H%M%S')
        # print(date_str)

        # 空の要素を含む行をフィルタリングして新しいリストを作成
        filtered_tsv = [row for row in tsv if any(cell.strip() for cell in row) or row[0] == '\"\"']
        filename = 'risyu' + date_str + '.tsv'
        with open(os.path.join(csvs_directory, filename), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            writer.writerows(filtered_tsv[2:])
            
        with open('output.tsv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            writer.writerows(filtered_tsv)

        for filtered_row in filtered_tsv[2:]:
            # print(filtered_row)
            ind_filename = 'risyu' + filtered_row[0] + '.tsv'
            filtered_row = date_str + '\t' + '\t'.join(filtered_row)
            with open(os.path.join(csvs_directory, ind_filename), 'a', newline='', encoding='utf-8') as csvfile:
                csvfile.write(filtered_row + '\n')
        time.sleep(250)
    except Exception as e:
        driver.quit()
        print('error')
        print(e)
        print(sys.exc_info())
        continue
try:
    while True:
        #os.mkdir('screenshots')
        # Setup Chrome options
        options = Options()
        #options.add_argument("--headless") # Ensure GUI is off. Remove this line if you want to see the browser navigating.
        
        # Set path to chromedriver as a service
        webdriver_service = Service(ChromeDriverManager().install())
        
        # Set the driver
        driver = webdriver.Chrome(service=webdriver_service, options=options)
        
        # Get website data
        driver.get("https://acanthus.cis.kanazawa-u.ac.jp/?lan=j")
        
        link = driver.find_element(By.LINK_TEXT, "ログイン")
        link.click()
        
        # Take a screenshot
        driver.implicitly_wait(5)
        driver.save_screenshot("screenshot.png")
        
        kuid = driver.find_element(By.ID, "kuid")
        passw = driver.find_element(By.ID, "password")
        
        kuid.clear()
        passw.clear()
        
        KUID = os.environ["KUID"]
        PASS = os.environ["KUPASS"]
        kuid.send_keys(KUID)
        passw.send_keys(PASS)
        
        driver.get_screenshot_as_file("screenshots2.png")
        
        driver.find_element(By.NAME, "_eventId_proceed").click()
        # Quit the driver
        
        driver.get_screenshot_as_file("screenshots3.png")
        
        #link = driver.find_element(By.LINK_TEXT, "既に回答しました")
        #link.click()
        
        element = driver.find_element(By.XPATH,"//a[span[text()='学務情報サービス']]")
        driver.execute_script("arguments[0].click();", element)
        
        all_handles = driver.window_handles
        
        driver.switch_to.window(all_handles[-1])
        
        print(driver.title)
        
        driver.get_screenshot_as_file("screenshots4.png")
        
        link = driver.find_element(By.XPATH, "//a[contains(., '履修・成績情報')]")
        link.click()
        
        driver.get_screenshot_as_file("screenshots5.png")
        
        link = driver.find_element(By.XPATH, "//a[contains(., '履修登録')]")
        link.click()
        
        driver.get_screenshot_as_file("screenshots7.png")
        
        for i in range(12 * 6):
            #print(1/0)
        
            driver.refresh()
            print(driver.window_handles)
         ##謎
            link = driver.find_element(By.XPATH, '//*[@id="ctl00_phContents_ucRegistEdit_lnkrationStatus"]')
            link.click()
    
            all_handles = driver.window_handles
    
            driver.switch_to.window(all_handles[-1])
    
            print(driver.title)
            print(driver.window_handles)
    
            with open('test.htm', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(driver.current_url)
        
                      
                    #状況クリック後
                    #0で全件表示
            print(driver.title)
            select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ctl00_phContents_ucRegistrationStatus_ddlLns_ddl"))
            )
            print("hoge")
            select_element = driver.find_element(By.ID, "ctl00_phContents_ucRegistrationStatus_ddlLns_ddl")
            select = Select(select_element)
            select.select_by_value('0')
                
            pdfurl = driver.current_url
            driver.get(pdfurl)
                
            source = 'page_source.html'
                
            page_source = driver.page_source
            with open(source, 'w', encoding='utf-8') as f:
                f.write(page_source)
                
            driver.close()
    
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[-1])
        
            #time.sleep(60 * 5)
            #time.sleep(10)

            #死活監視
            with open('deadoralive.json', 'r', encoding='utf-8') as f:
                deadoralive = json.load(f)
            
            deadoralive[scptname][scptname + str(toggle)] = int(time.time()/1)

            diff01 = abs(deadoralive[scptname][scptname + '0'] - deadoralive[scptname][scptname + '1'])
            deadoralive[scptname][scptname + '_diff'] = diff01

            with open('deadoralive.json', 'w', encoding='utf-8') as f:
                json.dump(deadoralive, f, indent=4)

            toggle = 1 - toggle

            current_second = time.localtime().tm_sec
            sleeptime = 60 - current_second
            time.sleep(sleeptime)       
        
        #time.sleep(1000)
        #driver.quit()
    
except:
    driver.quit()

    print('error')

