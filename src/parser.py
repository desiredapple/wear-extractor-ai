import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(options=options)

### LAMODA SECTION 

driver.get("https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3")
time.sleep(5)

catalog = driver.find_elements(By.XPATH,'//div[contains(@class, "gridItem")]')


print(catalog)

for url in catalog:

    driver.get(url)

    try:
        reviews_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "ui-product-page-reviews-tab") and contains(text(), "Отзывы")]'))
        )
        reviews_button.click()

        if not os.path.isdir("data"):
            os.mkdir("data")

        time.sleep(4)

        images = driver.find_elements(By.XPATH,'//img[contains(@class, "ui-reviews-gallery")]')
        
        for i, img in enumerate(images):
            cur_dir = f"data/{driver.title.split()[0]}"
            src = img.get_attribute("src")
            
            if not os.path.isdir(cur_dir):
                os.mkdir(cur_dir)
            if src:
                index = src.rfind(".")
                filename = f"{cur_dir}/sample_{i}.{src[index:]}"
                
            img_data = requests.get(src).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)

    except Exception as e:
        print("error:", e)

### END LAMODA SECTION

driver.quit()