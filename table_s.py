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

from selenium.webdriver.common.keys import Keys

import time
import  requests
import  os
import  json
import re

toggle = 0
scptname = '01seleniumer'

data = {}

fas = [
    "51",
    "52",
    "53",
    "54",
    "55",
    "-",
    "46"
]

with open('links_data.json', 'r', encoding='utf-8') as f:
    links_data = json.load(f)

# 今見ているページのうち表示テキストが"日"のaタグのリンク先をすべて配列に格納
def get_links(driver):
    time.sleep(2)
    results = {}
    #results = []
    table = driver.find_element(By.ID, "ctl00_phContents_ucGrid_grv")
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # ヘッダー行を除外
    #フッダ―行も除外
    rows = rows[:-1]
    for row in rows:
        if "日" in row.text:
            cells = row.find_elements(By.TAG_NAME, "td")  # 各行のセルを取得)
            #print(cells[1].text)
            ttcode = cells[1].text
            link_cell = cells[2]  # "日"リンクが含まれるセル
            p_faculty = cells[4].text  # 学類が含まれるセル
            teacher = cells[5].text  # 教員が含まれるセル
            q = cells[6].text  # クォーターが含まれるセル
            dp = cells[7].text  # 日時が含まれるセル
            #print(link_cell.find_element(By.TAG_NAME, "a").get_attribute('href'))
            #print(faculty_cell.text)

            ps = p_faculty.split("\n")

            if len(ps) == 3:
                iki = ps[0]
                rui = ps[1]
                title = ps[2]
            else:
                iki = ps[0]
                title = ps[1]
                rui = ""

            results[cells[1].text] = {
                "link": link_cell.find_element(By.TAG_NAME, "a").get_attribute('href'),
                "title": title,
                "iki": iki,
                "rui": rui,
                "teacher": teacher,
                "q": q,
                "dp": dp,
            }            
            #print(results)
            print(results[cells[1].text]['rui'])
            print(results[cells[1].text]['iki'])
        else:
            print('no')
    return results

pattern = r"lct_cd=([^&]+)"


for fa in fas:
    #try:
        #while True:
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
    #driver.get("http://localhost:8000/re.htm")

    a = False
    a = True
    if a:

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



        #link = driver.find_element(By.LINK_TEXT, "既に回答しました")
        #link.click()

        print('login')

        driver.execute_script("window.open('https://eduweb.sta.kanazawa-u.ac.jp/portal/Public/Syllabus/SearchMain.aspx');")
        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[-1])

        driver.get_screenshot_as_file("screenshots3.png")
        time.sleep(1)

        # 年度を2024年度に設定し、開講学域・研究科を融合学域に設定してから検索ボタンをクリックするコードを追加します。

        # 年度と開講学域・研究科のセレクトボックスを特定
        year_select = Select(driver.find_element(By.ID, "ctl00_phContents_ddl_year"))


        # 年度を2024年度に設定
        year_select.select_by_value("2024")
        print('year')
        driver.get_screenshot_as_file("screenshots4.png")

        # 開講学域・研究科を融合学域に設定
        faculty_select = Select(driver.find_element(By.ID, "ctl00_phContents_ddl_fac"))
        faculty_select.select_by_value(fa)

        print('faculty')
        # 検索ボタンをクリック
        search_button = driver.find_element(By.ID, "ctl00_phContents_ctl06_btnSearch")
        search_button.click()

    # 操作後のスクリーンショットを取得（オプション）
    time.sleep(2)
    driver.get_screenshot_as_file("screenshots5.png")

    # 年度と開講学域・研究科のセレクトボックスを特定した後のコードに追加
    lines_select = Select(driver.find_element(By.ID, "ctl00_phContents_ucGrid_ddlLines"))
    # 「全件」を選択
    lines_select.select_by_value("0")

    time.sleep(2)


    ja_links = get_links(driver)

    #pagination_links = driver.find_elements(By.XPATH, "//a[contains(@href, \"javascript:__doPostBack('ctl00$phContents$ucGrid$grv','Page$\")]")

    #print("page数", len(pagination_links))
    #current_page = 1
    #total_pages = len(pagination_links) + 1  # 最初のページを含めるために+1

    #while current_page <= total_pages:
    #    print(f"現在のページ: {current_page}")
    #    # ページ内のリンクを取得して処理
    #    ja_links.update(get_links(driver))
        
        # 次のページへ移動するためのリンクを取得
    #    pagination_links = driver.find_elements(By.XPATH, "//a[contains(@href, \"javascript:__doPostBack('ctl00$phContents$ucGrid$grv','Page$\")]")
    #    if current_page < total_pages:
    #        next_page_link = pagination_links[current_page - 1]  # current_pageは1から始まるため、インデックスとしては-1する
    #        next_page_link.click()
    #        time.sleep(2)  # ページ遷移の待機
    #        current_page += 1
    #    else:
    #        break  # 最後のページに達したら終了

    for key, value in ja_links.items():
        link = value.get("link", "")
        rui = value.get("rui", "")
        iki = value.get("iki", "")
        title = value.get("title", "")
        teacher = value.get("teacher", "")
        q = value.get("q", "")
        dp = value.get("dp", "")

        match = re.search(pattern, link)
        if match:
            lct_cd_value = match.group(1)
            #print(lct_cd_value)
            data[lct_cd_value] = {
                "link": link,
                "rui": rui,
                "iki": iki,
                "title": title,
                "teacher": teacher,
                "q": q,
                "dp": dp
            }
        else:
            print(f"lct_cdの値が見つかりませんでした。リンク: {link}")

    print(data)

    links_data.update(data)

    with open("links_data.json", "w", encoding="utf-8") as f:
        json.dump(links_data, f, ensure_ascii=False, indent=4)

    driver.quit()
    
#except:
#    driver.quit()

#    print('error')

#    print('error')
