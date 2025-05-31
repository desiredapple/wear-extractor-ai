from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import random
import time
import os


class Parser:

    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-background-networking")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_experimental_option(
            "prefs", {
                "profile.managed_default_content_settings.notifications": 2,
                "profile.managed_default_content_settings.media_stream": 2,
                "profile.managed_default_content_settings.stylesheets": 2,
                "profile.managed_default_content_settings.geolocation": 2,
                "profile.managed_default_content_settings.plugins": 2,
                "profile.managed_default_content_settings.images": 2,
                "profile.managed_default_content_settings.popups": 2,
                "profile.password_manager_enabled": False,
                "credentials_enable_service": False
            }
        )
        self.browser = uc.Chrome(options=options, log_level=3)
        self.wait = WebDriverWait(self.browser, 5)

    def parse_all(self):
        for k in range(1, 8):
            self.browser.get(
                f"https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3&page={k}")

            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')))
            page_catalog = [link.get_attribute('href') for link in self.browser.find_elements(
                By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')]

            Parser.parse_lamoda(self, page_catalog)

        for k in range(1, 8):
            self.browser.get(
                f"https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3&page={k}")

            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')))
            page_catalog = [link.get_attribute('href') for link in self.browser.find_elements(
                By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')]

            Parser.parse_lamoda(self.browser, page_catalog)
        self.browser.quit()

    def parse_lamoda(self, page_catalog):
        for item in page_catalog:

            self.browser.get(item)
            cur_dir = f"data/lamoda/{self.browser.title.split()[0]}"

            reviews_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[contains(@class, "ui-product-page-reviews-tab") and contains(text(), "Отзывы")]'))
            )
            reviews_button.click()

            if not os.path.isdir("data/lamoda"):
                os.makedirs("data/lamoda")

            if not os.path.isdir(cur_dir):
                os.mkdir(cur_dir)


            time.sleep(1)

            if self.browser.find_elements(
                    By.XPATH, '//img[contains(@class, "ui-reviews-gallery")]'):
                images_links = self.browser.find_elements(
                    By.XPATH, '//img[contains(@class, "ui-reviews-gallery")]')
            elif self.browser.find_elements(
                    By.XPATH, '//img[contains(@class, "photoAverage_9qw58_22")]'):
                images_links = self.browser.find_elements(
                    By.XPATH, '//img[contains(@class, "photoAverage_9qw58_22")]')
            else:
                continue


            if len(images_links) > 5:
                random.shuffle(images_links)
                images_links = images_links[:5]

            for img in images_links:
                src = img.get_attribute('src')
                if src.find('&') != -1:
                    src = src[:src.find('&')]

                i = 0
                if os.listdir(cur_dir):
                    i = max([int(el[el.find('_') + 1: el.find('.')])
                            for el in os.listdir(cur_dir)])

                if src:
                    extension_index = src.rfind('.')
                    filename = f"{cur_dir}/sample_{i + 1}.{src[extension_index + 1:]}"

                img_data = requests.get(src).content

                with open(filename, 'wb') as handler:
                    handler.write(img_data)
