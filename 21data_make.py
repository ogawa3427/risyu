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

toggle = 0
scptname = '21data_make'

csvs_directory = os.path.join(os.getcwd(), 'csvs')

while True:
    try:
        options = Options()
        options.add_argument("--headless") # Ensure GUI is off. Remove this line if you want to see the browser navigating.
        
        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=options)
        
        driver.get("https://acanthus.cis.kanazawa-u.ac.jp/?lan=j")
        link = driver.find_element(By.LINK_TEXT, "ログイン")
        link.click()
        
        # Take a screenshot
        driver.implicitly_wait(5)
        
        kuid = driver.find_element(By.ID, "kuid")
        passw = driver.find_element(By.ID, "password")
        
        kuid.clear()
        passw.clear()
        KUID = os.environ["KUID"]
        PASS = os.environ["KUPASS"]
        kuid.send_keys(KUID)
        passw.send_keys(PASS)
        
        driver.find_element(By.NAME, "_eventId_proceed").click()
                
        #link = driver.find_element(By.LINK_TEXT, "既に回答しました")
        #link.click()
        
        element = driver.find_element(By.XPATH,"//a[span[text()='学務情報サービス']]")
        driver.execute_script("arguments[0].click();", element)
        
        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[-1])
        print(driver.title)
        
        link = driver.find_element(By.XPATH, "//a[contains(., '履修・成績情報')]")
        link.click()
        
        link = driver.find_element(By.XPATH, "//a[contains(., '履修登録')]")
        link.click()
        
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
                
            page_source = driver.page_source               
            driver.close()
    
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[-1])


            #02
            mode = 0
            content=''
            name = ''
            lines = page_source.splitlines()
            for line in lines:
                if "ctl00_phContents_ucRegistrationStatus_lb" in line:
                    name = line
                if '						</tbody></table>' in line:
                    mode = 2
                if mode == 1:
                    if "</tr><tr" in line:
                        line = "eskape"
                    content += line
                if 'th align' in line:
                    mode = 1

            content = content.replace(" ", "")
            content = content.replace("\t", "")
            content = content.replace("\n", "")
            content = content.replace("</span>", "")
            content = re.sub(r'<span.*?>', '', content)
            content = re.sub(r'<td.*?>', '<td>', content)
            content = content.replace("</td><td>", ",")
            content = content.replace("<td>", "")
            content = content.replace("</td>", "")
            content = content.replace("&amp;", "&")
            content = re.sub(r'<\/tr>.*', '', content)

            content = re.sub(r'^\n', '', content)
            content = content.replace("eskape", "\n")
            #header = "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望"
            #contents = header + '\n' + content
            contents = content
            #こんなことしかできない自分のことが大嫌いだ
            contents = contents.replace("月2,火2", "月2，火2")

            name = re.sub(r'<.*?>', '', name)
            name = re.sub(r'\t', '', name)
            name = re.sub(r'[ :\/]', '', name)
            name = re.sub(r'\n', '', name)
            name = "risyu" + name
            name = name + ".csv"
            
            path = os.path.join(csvs_directory, name)
            with open(path, 'w', encoding='utf-8') as file:
                file.write(contents)

            print('CSV_made_sucsessfuly')
            print(path)


            ls = os.listdir(csvs_directory)
            ls = [ls for ls in ls if re.search("risyu", ls)]
            ls = [ls for ls in ls if re.search("csv", ls)]

            numlist = [re.findall(r'\d+', fname)[0] for fname in ls if re.findall(r'\d+', fname)]
            openfile = max(numlist)
            openfile = re.sub(r'^', 'risyu', openfile)
            openfile = re.sub(r'$', '.csv', openfile)
            # 'csvs'ディレクトリ内のファイルを開く
            with open(os.path.join(csvs_directory, openfile), 'r', encoding='utf-8') as f:
                theline = ''.join(line for line in f if True)
                theline = re.sub('\n','eskape', theline)

            asof = max(numlist)
            patt = r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})"
            repl = r"\1年\2月\3日\4:\5:\6現在"
            asof = re.sub(patt, repl, asof)


        #lines = rowdata.splitlines()
        #reader = csv.reader(lines)
        #jsondata = json.dumps(list(reader), ensure_ascii=False)
            data = {
                #'header' : "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望",
                'header' : "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,登録数,残数",
                'csv': theline,
                'asof': asof
            }
            with open('recieved.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print('json_made_sucsessfuly')
        
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
            sleeptime = 300 - current_second
            time.sleep(sleeptime)
    
    except:
        driver.quit()
        print(2/0)

        print('error')

