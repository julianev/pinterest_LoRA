import os, time, requests, re, csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from uuid import uuid4

class PinterestScraper:

    def __init__(self, search_query:str=None, user_name:str=None, board_name:str=None, num_images:int=50):
        self.num_images = num_images
        if search_query:
            self.url = f"https://www.pinterest.com/search/pins/?q={search_query}"
            self.dir_name = "pinterest_images_" + search_query.replace(' ', '_')
        else:
            self.url = f"https://www.pinterest.com/{user_name}/{board_name}/"
            self.dir_name = "pinterest_images_" + user_name + '_' + board_name

    def run(self):
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)

        metadata_file = os.path.join(self.dir_name, 'metadata.csv')
        with open(metadata_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['file_name', 'caption'])

        chromedriver_path = './chromedriver'
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)
        driver.get(self.url)
        time.sleep(6) # load page
        body = driver.find_element(By.TAG_NAME, "body")

        scroll_pause_time = 5
        used_img_download_urls = set()
        while len(used_img_download_urls) <= self.num_images:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            pins = soup.find_all("div", {"data-test-id": "pin-visual-wrapper"})
            for pin_div in pins:
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
                if num_used_urls < len(used_img_download_urls) & len(used_img_download_urls) <= self.num_images:
                    #print(img_download_url)
                    img_data = requests.get(img_download_url).content
                    file_name = f"{uuid4()}.jpg"
                    file_path = os.path.join(self.dir_name, file_name)
                    with open(file_path, "wb") as handler:
                        handler.write(img_data)
                    
                    # append image caption to csv file
                    img_caption = img["alt"]
                    with open(metadata_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([file_name, img_caption])
            
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(scroll_pause_time)
        
        driver.quit()