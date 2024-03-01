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

with open('links_data.json', 'r', encoding='utf-8') as f:
    links_data = json.load(f)

# 今見ているページのうち表示テキストが"日"のaタグのリンク先をすべて配列に格納
def get_links(driver):
    links = driver.find_elements(By.XPATH, "//a[contains(., '日')]")
    links = [link.get_attribute("href") for link in links]
    return links

pattern = r"lct_cd=([^&]+)"

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

if not os.path.exists('./htmls'):
    os.makedirs('./htmls')

# Get website data
for code, info in links_data.items():
    link = info["link"]
    driver.get(link)
    html_data = driver.page_source
    file_path = f"./htmls/{code}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_data)
    print(f"{code}のHTMLを保存しました。")

driver.quit()