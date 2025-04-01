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
import pytz

toggle = 0
scptname = '21data_make'

csvs_directory = os.path.join(os.getcwd(), 'csvs')

while True:
    try:
        options = Options()
        options.add_argument("--headless") # Ensure GUI is off. Remove this line if you want to see the browser navigating.
        
        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=options)
        
        # 直接URLにアクセス
        driver.get("https://eduweb.sta.kanazawa-u.ac.jp/portal/Public/Regist/RegistrationStatus.aspx?year=2025&lct_term_cd=11")
        
        # 全件表示のセレクトボックスを待機して選択
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_phContents_ucRegistrationStatus_ddlLns_ddl"))
        )
        select = Select(select_element)
        select.select_by_value('0')  # 全件表示
        
        # ページの内容を取得
        page_source = driver.page_source
        
        # 以下、既存の処理を継続
        mode = 0
        content = ''
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

        # 現在時刻を取得（JST）
        jst = pytz.timezone('Asia/Tokyo')
        current_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time() + 9 * 3600))
        valid_status = "valid"

        # TSVファイル用のデータを作成
        tsv_contents = f"{current_time}\t{valid_status}\n"
        tsv_contents += "時間割番号\t科目区分\t時間割名\t曜日時限\t教員名\t対象学生\t適正人数\t全登録数\t優先指定\t第１希望\t第２希望\t第３希望\t第４希望\t第５希望\n"
        for line in contents.split('\n'):
            if line.strip():
                tsv_contents += line.replace(',', '\t') + '\n'

        # TSVファイルを保存
        tsv_path = os.path.join('output.tsv')
        with open(tsv_path, 'w', encoding='utf-8') as file:
            file.write(tsv_contents)

        print('TSV_made_successfully')
        print(tsv_path)

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
            'header' : "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,全登録数,優先指定,第１希望,第２希望,第３希望,第４希望,第５希望",
            #'header' : "時間割番号,科目区分,時間割名,曜日時限,教員名,対象学生,適正人数,登録数,残数",
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

