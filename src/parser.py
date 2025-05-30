import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

browser = uc.Chrome(options=options)

### LAMODA SECTION 

browser.get("https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3")

time.sleep(3)

page_catalog = [link.get_attribute('href') for link in browser.find_elements(By.XPATH,'//a[contains(@class, "x-product-card__pic-catalog")]')]

for item in page_catalog:

    browser.get(item)

    try:
        reviews_button = WebDriverWait(browser, 15.).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "ui-product-page-reviews-tab") and contains(text(), "Отзывы")]'))
        )
        reviews_button.click()

        if not os.path.isdir("data"):
            os.mkdir("data")
            os.mkdir("data/lamoda")

        time.sleep(5)

        images = browser.find_elements(By.XPATH,'//img[contains(@class, "ui-reviews-gallery")]')
        if not images:
            images = browser.find_elements(By.XPATH,'//img[contains(@class, "_photoAverage_9qw58_22")]')
        cur_dir = f"data/lamoda/{browser.title.split()[0]}"
        if not os.path.isdir(cur_dir):
            os.mkdir(cur_dir)
        
        i = 0
        for img in images:
            src = img.get_attribute('src')
            
            if os.listdir(cur_dir):
                i = max([int(el[el.find('_') + 1 : el.find('.')]) for el in os.listdir(cur_dir)])
                
            if src:
                index = src.rfind('.')
                filename = f"{cur_dir}/sample_{i + 1}.{src[index + 1:]}"
            
            img_data = requests.get(src).content
                
            with open(filename, 'wb') as handler:
                handler.write(img_data)

    except Exception as e:
        print("error:", e)

### END LAMODA SECTION

browser.quit()