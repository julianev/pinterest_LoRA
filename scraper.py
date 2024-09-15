import os, time, requests, re, csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from uuid import uuid4

search_query = "pattern wavy"
dir_name = "pinterest_images_" + search_query.replace(' ', '_')
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

metadata_file = os.path.join(dir_name, 'metadata.csv')
with open(metadata_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['file_name', 'caption'])

chromedriver_path = './chromedriver'
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
url = f"https://www.pinterest.com/search/pins/?q={search_query}"
driver.get(url)
time.sleep(6) # load page

scroll_count = 5
scroll_pause_time = 5
used_img_download_urls = set()
body = driver.find_element(By.TAG_NAME, "body")
for count in range(scroll_count):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    pins = soup.find_all("div", {"data-test-id": "pin-visual-wrapper"})
    #print("len", len(pins))

    for idx, pin_div in enumerate(pins):
        img = pin_div.find("img", {"src": True})
        img_url = img["src"]
        match = re.search(r'(https:\/\/i\.pinimg\.com\/\d{3}x\/)(.*)', img_url)
        if match is None:
            continue
        extracted_part = match.group(2) # extract second part of url and construct download url for higher quality image
        img_download_url = os.path.join('https://i.pinimg.com/736x/', extracted_part)

        num_used_urls = len(used_img_download_urls)
        used_img_download_urls.add(img_download_url)
        # only download image if not already visited
        if num_used_urls < len(used_img_download_urls):
            #print(img_download_url)
            img_data = requests.get(img_download_url).content
            file_name = f"{uuid4()}.jpg"
            file_path = os.path.join(dir_name, file_name)
            with open(file_path, "wb") as handler:
                handler.write(img_data)
            
            # get image caption
            img_caption = img["alt"]
            #print(title)
            with open(metadata_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Append a new row (replace with your actual data)
                writer.writerow([file_name, img_caption])
    
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(scroll_pause_time)

#driver.quit()