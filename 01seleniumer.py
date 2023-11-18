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

toggle = 0

try:
    while True:
        #os.mkdir('screenshots')
        # Setup Chrome options
        options = Options()
        options.add_argument("--headless") # Ensure GUI is off. Remove this line if you want to see the browser navigating.
        
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

            current_second = time.localtime().tm_sec
            sleeptime = 60 - current_second
            time.sleep(sleeptime)

            #死活監視
            with open('deadoralive.json', 'r', encoding='utf-8') as f:
                deadoralive = json.load(f)
            
            deadoralive['01seleniumer' + toggle] = time.time()

            with open('deadoralive.json', 'w', encoding='utf-8') as f:
                json.dump(deadoralive, f, indent=4)

            toggle = 1 - toggle

        
        
        #time.sleep(1000)
        #driver.quit()
    
except:
    driver.quit()

    print('error')

