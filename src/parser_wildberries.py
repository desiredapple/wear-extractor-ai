from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
        # mutual_list = ["https://www.wildberries.ru/catalog/{k}/odezhda/bryuki-i-shorty",
        #                "https://www.wildberries.ru/catalog/{k}/odezhda/verhnyaya-odezhda",
        #                "https://www.wildberries.ru/catalog/{k}/odezhda/dzhempery-i-kardigany",
        #                "https://www.wildberries.ru/catalog/{k}/odezhda/kostyumy",
        #                "https://www.wildberries.ru/catalog/{k}/odezhda/longslivy",
        #                "https://www.wildberries.ru/catalog/{k}/odezhda/pidzhaki-i-zhakety",
        #                "https://www.wildberries.ru/catalog/{k}/odezhda/tolstovki",
        #                "https://www.wildberries.ru/catalog/{k}/odezhda/bryuki-i-shorty/shorty",
        #                ]

        female_list = ["https://www.wildberries.ru/catalog/zhenshchinam/odezhda/bluzki-i-rubashki",
                       "https://www.wildberries.ru/catalog/zhenshchinam/odezhda/dzhinsy-dzhegginsy",
                       "https://www.wildberries.ru/catalog/zhenshchinam/odezhda/kombinezony-polukombinezony",
                       "https://www.wildberries.ru/catalog/zhenshchinam/odezhda/platya",
                       "https://www.wildberries.ru/catalog/zhenshchinam/odezhda/tuniki",
                       "https://www.wildberries.ru/catalog/zhenshchinam/odezhda/futbolki-i-topy",
                       "https://www.wildberries.ru/catalog/zhenshchinam/odezhda-dlya-doma/halaty",
                       "https://www.wildberries.ru/catalog/zhenshchinam/odezhda/yubki"]

        male_list = ["https://www.wildberries.ru/catalog/muzhchinam/odezhda/dzhinsy",
                     "https://www.wildberries.ru/catalog/muzhchinam/odezhda/kombinezony",
                     "https://www.wildberries.ru/catalog/muzhchinam/pizhamy",
                     "https://www.wildberries.ru/catalog/muzhchinam/odezhda/rubashki",
                     "https://www.wildberries.ru/catalog/muzhchinam/odezhda/futbolki-i-mayki",
                     "https://www.wildberries.ru/catalog/muzhchinam/halaty",
                     "https://www.wildberries.ru/catalog/muzhchinam/bele"]

        for link in (female_list + male_list):
            self.browser.get(link)

            self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "product-card__wrapper")))
            actions = ActionChains(self.browser)

            start = self.browser.find_element(
                By.CLASS_NAME, "catalog-title-wrap")
            end = self.browser.find_element(
                By.CLASS_NAME, "catalog-page__search-tags")

            for _ in range(5):
                actions.move_to_element(end).perform()
                actions.move_to_element(start).perform()

            page_catalog = [link.get_attribute('href') for link in self.browser.find_elements(
                By.XPATH, '//a[contains(@class, "product-card__link")]')]

            self.__parse_wildberries(page_catalog)

        self.browser.quit()

    def __parse_wildberries(self, page_catalog):
        cur_dir = "data/wildberries"

        if not os.path.isdir(f"{cur_dir}/showcase") and not os.path.isdir(f"{cur_dir}/review_gallery"):
            os.makedirs(f"{cur_dir}/showcase")
            os.makedirs(f"{cur_dir}/review_gallery")

        for item in page_catalog:

            self.browser.get(item)

            self.wait.until(EC.presence_of_element_located((
                By.CLASS_NAME, "product-page__link-category")))

            category = self.browser.find_element(
                By.CLASS_NAME, "product-page__link-category").get_attribute("innerHTML")

            showcase_images_links = self.browser.find_elements(
                By.XPATH, '//li[contains(@class, "j-product-photo")]')[:3]
            showcase_images_links = [elem.find_element(
                By.TAG_NAME, 'img') for elem in showcase_images_links]

            actions = ActionChains(self.browser)

            
            end = self.browser.find_element(
                By.XPATH, '//div[contains(@class, "user-activity__tab-content")]')

            actions.move_to_element(end).perform()
            
            self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "comments__content")))

            self.wait.until(EC.presence_of_element_located((
                By.XPATH, '//div[contains(@class, "swiper-slide img-plug")]')))
            
            reviews_images_links = self.browser.find_elements(
                By.XPATH, '//div[contains(@class, "swiper-slide img-plug")]')
            
            reviews_images_links = [elem.find_element(
                By.TAG_NAME, "img") for elem in reviews_images_links]

            if len(reviews_images_links) > 5:
                random.shuffle(reviews_images_links)
                reviews_images_links = reviews_images_links[:5]

            if len(showcase_images_links) > 0 and not os.path.isdir(f"{cur_dir}/showcase/{category}"):
                os.mkdir(f"{cur_dir}/showcase/{category}")

            if len(reviews_images_links) > 0 and not os.path.isdir(f"{cur_dir}/review_gallery/{category}"):
                os.mkdir(f"{cur_dir}/review_gallery/{category}")

            for img in (showcase_images_links + reviews_images_links):

                src = img.get_attribute('src')

                image_type = "review_gallery" if img in reviews_images_links else "showcase"

                if image_type == "review_gallery":
                    src = src[:src.rfind('/')] + "/fs.webp"
                else:
                    index = src.find("images")
                    rplc = src[index + src[index:].find('/') + 1 : src.rfind('/')]
                    src = src.replace(rplc, "big")
                
                
                if os.path.exists(f"{cur_dir}/{image_type}/{category}/{category}_{image_type}_stats_log.txt"):
                    with open(f"{cur_dir}/{image_type}/{category}/{category}_{image_type}_stats_log.txt", 'r') as handler:
                        if src in [str.split()[1] for str in handler.readlines()]:
                            break

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
