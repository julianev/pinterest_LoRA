from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
import os

def scroll_down(driver, scroll_pause_time=5, scroll_count=30):
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(scroll_count):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(scroll_pause_time)

search_query = "pattern wavy"
dir_name = "pinterest_images_" + search_query.replace(' ', '_')
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

chromedriver_path = r'/home/jule/projects/LoRA/chromedriver'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
url = f"https://www.pinterest.com/search/pins/?q={search_query}"
driver.get(url)
time.sleep(6)  # time for the page to load
scroll_down(driver)

soup = BeautifulSoup(driver.page_source, "html.parser")
pins = soup.find_all("div", {"data-test-id": "pin-visual-wrapper"})

for idx, pin_div in enumerate(pins):
    img = pin_div.find("img", {"src": True})
    img_url = img["src"]
    img_data = requests.get(img_url).content
    file_path = os.path.join(dir_name, f"img_{idx}.jpg")
    with open(file_path, "wb") as handler:
        handler.write(img_data)
    title = img["alt"]
    print(title)

#driver.quit()