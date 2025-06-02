import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import random
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
        self.wait = WebDriverWait(self.browser, 15)
        self.actions = ActionChains(self.browser)

    def parse_all(self):
        parsing_list = ["https://www.wildberries.ru/brands/7049-mark-formelle/all",
                        "https://www.wildberries.ru/brands/1836-finn-flare/all",
                        "https://www.wildberries.ru/brands/290923899-maag/all",
                        "https://www.wildberries.ru/brands/gloria-jeans/all",
                        "https://www.wildberries.ru/brands/zarina/all",
                        "https://www.wildberries.ru/brands/befree/all",
                        "https://www.wildberries.ru/brands/mango/all",
                        "https://www.wildberries.ru/brands/baon/all",
                        "https://www.wildberries.ru/brands/sela/all/"
                        ]
        parsing_list_with_odezdha = ["https://www.wildberries.ru/brands/1092023-mabag-eco/odezhda/",
                                     "https://www.wildberries.ru/brands/love-republic/odezhda/",
                                     "https://www.wildberries.ru/brands/urban-tiger/odezhda/",
                                     "https://www.wildberries.ru/brands/elis-24907/odezhda/",
                                     "https://www.wildberries.ru/brands/ivolga/odezhda/",
                                     "https://www.wildberries.ru/brands/mollis/odezhda/",
                                     "https://www.wildberries.ru/brands/ostin/odezhda/",
                                     "https://www.wildberries.ru/brands/pompa/odezhda/",
                                     "https://www.wildberries.ru/brands/emka/odezhda/",
                                     ]

        for link in (parsing_list + parsing_list_with_odezdha):
            for i in range(1, 4):
                self.browser.get(f"{link}?sort=popular&page={i}")

                self.wait.until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "product-card__wrapper")))

                start = self.browser.find_element(
                    By.CLASS_NAME, "catalog-title-wrap")
                end = self.browser.find_element(
                    By.TAG_NAME, "footer")

                for _ in range(5):
                    self.actions.move_to_element(end).perform()
                    self.actions.move_to_element(start).perform()

                page_catalog = [link.get_attribute('href') for link in self.browser.find_elements(
                    By.XPATH, '//a[contains(@class, "product-card__link")]')]

                self.__parse_wildberries(page_catalog)

        self.browser.quit()

    def __parse_wildberries(self, page_catalog):

        cur_dir = "data/wildberries"

        if not os.path.isdir(f"{cur_dir}/showcase") and not os.path.isdir(f"{cur_dir}/review_gallery") and not os.path.isdir("log"):
            os.makedirs(f"{cur_dir}/showcase")
            os.makedirs(f"{cur_dir}/review_gallery")
            os.mkdir("log")

        for item in page_catalog:

            self.browser.get(item)

            self.wait.until(EC.presence_of_element_located((
                By.CLASS_NAME, "product-page__link-category")))


# ['shirt, blouse', 'top, t-shirt, sweatshirt', 'sweater', 'cardigan', 'jacket', 'vest', 'pants', 'shorts', 'skirt', 'coat',
# 'dress', 'jumpsuit', 'cape', 'glasses', 'hat', 'headband, head covering, hair accessory', 'tie', 'glove', 'watch', 'belt',
# 'leg warmer', 'tights, stockings', 'sock', 'shoe', 'bag, wallet', 'scarf', 'umbrella', 'hood', 'collar', 'lapel', 'epaulette',
# 'sleeve', 'pocket', 'neckline', 'buckle', 'zipper', 'applique', 'bead', 'bow', 'flower', 'fringe', 'ribbon', 'rivet', 'ruffle', 'sequin', 'tassel']

            category = self.browser.find_element(
                By.CLASS_NAME, "product-page__link-category").get_attribute("innerHTML")

            showcase_images_links = self.browser.find_elements(
                By.XPATH, '//li[contains(@class, "j-product-photo")]')[:4]
            showcase_images_links = [elem.find_element(
                By.TAG_NAME, 'img') for elem in showcase_images_links]

            actions = ActionChains(self.browser)

            end = self.browser.find_element(
                By.XPATH, '//div[contains(@class, "user-activity__tab-content")]')

            actions.move_to_element(end).perform()

            self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "comments__content")))

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
                    rplc = src[index +
                               src[index:].find('/') + 1: src.rfind('/')]
                    src = src.replace(rplc, "big")

                if os.path.exists(f"log/{category}_{image_type}_stats_log.txt"):
                    with open(f"log/{category}_{image_type}_stats_log.txt", 'r') as handler:
                        if src in [str.split()[1] for str in handler.readlines()]:
                            break

                i = 0
                if len([filename for filename in os.listdir(f"{cur_dir}/{image_type}/{category}") if filename.split('_')[-1].split('.')[0].isdigit()]) > 0:
                    i = max([int(el.split('_')[-1].split('.')[0]) for el in os.listdir(
                        f"{cur_dir}/{image_type}/{category}") if el.split('_')[-1].split('.')[0].isdigit()])

                with open(f"log/{category}_{image_type}_stats_log.txt", 'a') as handler:
                    handler.write(f"{i}. {src}\n")

                with open("log/stats.log", 'w') as file:
                    stats = [f"{r} - {len(files)}\n" for r,
                             _, files in os.walk(f"./{cur_dir}")]
                    review_number = sum(
                        [int(st.split()[-1]) if st.find("review_gallery") != -1 else 0 for st in stats])
                    showcase_number = sum(
                        [int(st.split()[-1]) if st.find("showcase") != -1 else 0 for st in stats])
                    stats.append(f"review all - {review_number}\n")
                    stats.append(f"showcase all - {showcase_number}\n")
                    file.writelines(stats[1:])

                extension_index = src.rfind('.')
                filename = f"{cur_dir}/{image_type}/{category}/sample_{i + 1}.{src[extension_index + 1:]}"

                img_data = requests.get(src).content

                with open(filename, 'wb') as handler:
                    handler.write(img_data)


a = Parser()
a.parse_all()
