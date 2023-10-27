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

link = driver.find_element(By.XPATH, "//a[contains(., '履修時間割表')]")
link.click()

driver.get_screenshot_as_file("screenshots7.png")


pdfurl = driver.current_url
driver.get(pdfurl)


page_source = driver.page_source
with open('page_source.html', 'w', encoding='utf-8') as f:
    f.write(page_source)

time.sleep(1000)
driver.quit()
