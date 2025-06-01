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
        self.wait = WebDriverWait(self.browser, 7)

    def parse_all(self):

        for k in range(1, 8):
            self.browser.get(
                f"https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3&page={k}")

            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')))

            page_catalog = [link.get_attribute('href') for link in self.browser.find_elements(
                By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')]

            Parser.__parse_lamoda(self, page_catalog)

        for k in range(1, 8):
            self.browser.get(
                f"https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3&page={k}")

            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')))

            page_catalog = [link.get_attribute('href') for link in self.browser.find_elements(
                By.XPATH, '//a[contains(@class, "x-product-card__pic-catalog")]')]

            Parser.__parse_lamoda(self.browser, page_catalog)
        self.browser.quit()

    def __parse_lamoda(self, page_catalog):
        cur_dir = "data/lamoda"

        if not os.path.isdir(f"{cur_dir}/showcase") and not os.path.isdir(f"{cur_dir}/review_gallery"):
            os.makedirs(f"{cur_dir}/showcase")
            os.makedirs(f"{cur_dir}/review_gallery")

        for item in page_catalog:

            self.browser.get(item)
            category = self.browser.title.split()[0]

            reviews_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[contains(@class, "ui-product-page-reviews-tab") and contains(text(), "Отзывы")]'))
            )
            reviews_button.click()

            time.sleep(3)

            showcase_images_links = self.browser.find_elements(
                By.XPATH, '//div[contains(@class, "ui-product-page-gallery")]')[:3]
            showcase_images_links = [elem.find_element(
                By.TAG_NAME, 'img') for elem in showcase_images_links]

            if self.browser.find_elements(
                    By.XPATH, '//img[contains(@class, "ui-reviews-gallery")]'):
                reviews_images_links = self.browser.find_elements(
                    By.XPATH, '//img[contains(@class, "ui-reviews-gallery")]')
            else:
                reviews_images_links = self.browser.find_elements(
                    By.XPATH, '//img[contains(@class, "photoAverage_9qw58_22")]')

            if len(reviews_images_links) > 5:
                random.shuffle(reviews_images_links)
                reviews_images_links = reviews_images_links[:5]

            if len(showcase_images_links) > 1 and not os.path.isdir(f"{cur_dir}/showcase/{category}"):
                os.mkdir(f"{cur_dir}/showcase/{category}")

            if len(reviews_images_links) > 1 and not os.path.isdir(f"{cur_dir}/review_gallery/{category}"):
                os.mkdir(f"{cur_dir}/review_gallery/{category}")

            for img in (showcase_images_links + reviews_images_links):

                src = img.get_attribute('src')
                if src.find('&') != -1:
                    src = src[:src.find('&')]

                image_type = "review_gallery" if img in reviews_images_links else "showcase"

                if os.path.exists(f"{cur_dir}/{image_type}/{category}/{category}_{image_type}_stats_log.txt"):
                    with open(f"{cur_dir}/{image_type}/{category}/{category}_{image_type}_stats_log.txt", 'r') as handler:
                        if src in [str.split()[1] for str in handler.readlines()]:
                            continue

                i = 0
                if len([filename for filename in os.listdir(f"{cur_dir}/{image_type}/{category}") if filename.split('_')[-1].split('.')[0].isdigit()]) > 0:
                    i = max([int(el.split('_')[-1].split('.')[0]) for el in os.listdir(
                        f"{cur_dir}/{image_type}/{category}") if el.split('_')[-1].split('.')[0].isdigit()])

                with open(f"{cur_dir}/{image_type}/{category}/{category}_{image_type}_stats_log.txt", 'a') as handler:
                    handler.write(f"{i}. {src}\n")

                extension_index = src.rfind('.')
                filename = f"{cur_dir}/{image_type}/{category}/sample_{i + 1}.{src[extension_index + 1:]}"

                img_data = requests.get(src).content

                with open(filename, 'wb') as handler:
                    handler.write(img_data)


a = Parser()
a.parse_all()
