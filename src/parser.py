from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import random
import os

options = uc.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-sync")
options.add_argument("--metrics-recording-only")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option(
    "prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.notifications": 2,
        "profile.managed_default_content_settings.media_stream": 2
    }
)

browser = uc.Chrome(options=options, log_level=3)
wait = WebDriverWait(browser, 10)

### LAMODA SECTION
for k in range(1, 14):
    browser.get(f"https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3&page={k}")


    wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')))
    page_catalog = [link.get_attribute('href') for link in browser.find_elements(By.XPATH,'//a[contains(@class, "x-product-card__pic-catalog")]')]

    for item in page_catalog:

        browser.get(item)

        try:
            reviews_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "ui-product-page-reviews-tab") and contains(text(), "Отзывы")]'))
            )
            reviews_button.click()

            if not os.path.isdir("data"):
                os.mkdir("data")
                os.mkdir("data/lamoda")

            wait.until(EC.presence_of_element_located((By.XPATH,'//img[contains(@class, "ui-reviews-gallery")]')))

            images = browser.find_elements(By.XPATH,'//img[contains(@class, "ui-reviews-gallery")]')
            if not images:
                images = browser.find_elements(By.XPATH,'//img[contains(@class, "_photoAverage_9qw58_22")]')

            cur_dir = f"data/lamoda/{browser.title.split()[0]}"
            if not os.path.isdir(cur_dir):
                os.mkdir(cur_dir)
            
            i = 0
            
            if len(images) > 5:
                random.shuffle(images)
                images = images[:5]
            
            for img in images:
                src = img.get_attribute('src')
                if src.find('&') != -1:
                    src = src[:src.find('&')]
                
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