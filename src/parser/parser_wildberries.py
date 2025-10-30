"""Wildberries class-parser

Parse photos from comments and gallery sections of most popular positions from certain shops listed in the code. 
"""

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from datetime import datetime
import requests
import random
import time
import os

import helpers.counter

class WildberriesParser:
    def __init__(self):
        """Initializes a browser instance.

        The options should include built-in optimization with an initialized browser.
        Also contain list of specified categories allowed for parsing.
        """
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
        options.add_experimental_option("prefs", {
                "profile.managed_default_content_settings.notifications": 2,
                "profile.managed_default_content_settings.media_stream": 2,
                "profile.managed_default_content_settings.stylesheets": 2,
                "profile.managed_default_content_settings.geolocation": 2,
                "profile.managed_default_content_settings.plugins": 2,
                "profile.managed_default_content_settings.images": 2,
                "profile.managed_default_content_settings.popups": 2,
                "profile.password_manager_enabled": False,
                "credentials_enable_service": False, },
                )
        self.browser = uc.Chrome(version_main=141, browser_executable_path="/snap/bin/chromium", options=options, log_level=3)
        self.wait = WebDriverWait(self.browser, 15)
        self.actions = ActionChains(self.browser)

        self.categories = {
            "Blouse": ["Блузки", "Блузки-боди"],
            "Cape": ["Плащи", "Тренчкоты"],
            "Cardigan": [
                "Водолазки",
                "Термоводолазки",
                "Джемперы",
                "Кардиганы",
                "Джемпер спортивный",
                "Пуловеры",
                "Свитшоты",
            ],
            "Coat": ["Пальто", "Полупальто"],
            "Dress": ["Платья", "Сарафаны", "Платья спортивное", "Туники"],
            "Gloves": ["Перчатки", "Варежки", "Митенки"],
            "Hat": [
                "Балаклавы",
                "Бейсболки",
                "Панамы",
                "Кепи",
                "Шапки",
                "Шапки-ушанка",
                "Шляпы",
                "Шапки-шлем",
                "Козырьки",
                "Береты",
            ],
            "Jacket": [
                "Анорак",
                "Бомберы",
                "Жакеты",
                "Куртки",
                "Пиджаки",
                "Куртка спортивная",
                "Ветровки",
                "Косухи",
            ],
            "Jumpsuit": ["Комбинезоны", "Полукомбинезоны"],
            "Longsleeve": [
                "Лонгсливы",
                "Рашгард",
                "Лонгсливы спортивные",
                "Термолонгсливы",
            ],
            "Pants": [
                "Бриджи",
                "Бриджи спортивные",
                "Брюки",
                "Брюки спортивные",
                "Велосипедки",
                "Джеггинсы",
                "Джинсы",
                "Леггинсы",
                "Тайтсы",
                "Капри",
            ],
            "Scarf": ["Платки", "Палантин", "Шарфы", "Снуды"],
            "Shirt": ["Рубашки"],
            "Shorts": ["Бордшорты", "Шорты", "Шорты спортивные", "Бермуды"],
            "Skirt": ["Юбки спортивные", "Юбки"],
            "Sweater": ["Свитеры", "Кофты"],
            "Sweatshirt": ["Толстовки", "Толстовки спортивная", "Худи"],
            "T-shirt, Polo": [
                "Футболки",
                "Футболка спортивная",
                "Футболки-поло",
                "Термофутболки",
                "Майки спортивные",
                "Манишки",
            ],
            "Top": ["Топ"],
            "Underwear": [
                "Боди",
                "Кальсоны",
                "Комплект белья",
                "Леггинсы ч/н",
                "Майки бельевые",
                "Неглиже",
                "Ночные сорочки",
                "Пижамы",
                "Плавки",
                "Термободи",
                "Трусы",
                "Кальсоны спортивные",
                "Корсет",
                "Пеньюар",
            ],
            "Vest": ["Жилеты"],
            "Winter Jacket": ["Пуховики", "Дубленки", "Парки", "Шубы искусственные"],
            "Belt": ["Ремни", "Пояса"],
            "Shoes": [
                "Босоножки",
                "Сандалии",
                "Сабо",
                "Полусапожки",
                "Мокасины",
                "Лоферы",
                "Балетки",
                "Кеды",
                "Туфли",
                "Ботинки",
                "Полуботинки",
                "Мюли",
                "Кроссовки",
                "Ледоступы",
                "Резиновые сапоги",
                "Сапоги",
                "Ботильоны",
                "Угги",
                "Ботфорты",
                "Дутики",
            ],
            "Stockings": ["Гольфы", "Колготки", "Термоколготки", "Гетры"]
            #            Commented categories (unnecesary)
            #            "Bag": ["Рюкзак", "Сумка", "Сумка-шоппер", "Сумка спортивная"]
            #            "Bra": ["Бюстгальтер", "Лиф для купальника", "Топ спортивный"],
            #            "Socks": ["Носки", "Подследники", "Термоноски"],
            #            "Sunglasses": ["Солнцезащитные очки"],
        }


    def _get_category(self, item_name: str) -> str:
        """Check whether the category is among the ones that need to be parsed."""
        item_name = item_name.lower()

        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in item_name:
                    return category

        return "None"


    def _parse_process(self, page_catalog: list) -> None:
        """From selected page method gets photos from both of gallery and comments sections."""
        data_dir = "data/wildberries"

        # Create directories if doesn't exist.
        if not os.path.isdir(f"{data_dir}/showcase"):
            os.makedirs(f"{data_dir}/showcase")
        if not os.path.isdir(f"{data_dir}/review_gallery"):
            os.makedirs(f"{data_dir}/review_gallery")

        for item in page_catalog:
            self.browser.get(item)

            # Wait for page for full load (it's starts to load from category).
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "categoryLinkCategory--VSJ8c")]')))

                for _ in range(3):
                    try:
                        category_elem = self.browser.find_element(By.XPATH, '//span[contains(@class, "categoryLinkCategory--VSJ8c")]')
                        category_html = category_elem.get_attribute("innerHTML")
                        category = self._get_category(category_html)
                        break
                    except StaleElementReferenceException:
                        time.sleep(0.3)

            except TimeoutException:
                category = None
                pass


            # Skip if the category not in parse list.
            if category == "None":
                continue

            # Get page ID.
            item_id = item[item.find("catalog") + len("catalog") + 1 : item.rfind("/")]


            # Get showcase images links. 
            showcase_classes = self.browser.find_elements(
                By.XPATH,
                '//div[contains(@class, "swiper-slide miniatureSlide--acvJc")]',
            )
            showcase_images_links = [
                elem.find_element(By.TAG_NAME, "img").get_attribute("src")
                for elem in showcase_classes
            ]


            # Scroll to review section for script to display review photos.
            review_section = self.browser.find_element(By.ID, "product-feedbacks")
            self.actions.move_to_element(review_section).perform()
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "product-feedbacks__user-photos")]')))
            except TimeoutException:
                continue


            # Get review images links. 
            review_classes = self.browser.find_elements(
                By.XPATH, '//img[contains(@class, "image--CJ2Ug")]'
            )
            review_image_links = [elem.get_attribute("src") for elem in review_classes]

            
            if len(review_image_links) and len(showcase_images_links):
                # Create category's directory.
                if not os.path.isdir(f"{data_dir}/showcase/{category}"):
                    os.makedirs(f"{data_dir}/showcase/{category}")
                if not os.path.isdir(f"{data_dir}/review_gallery/{category}"):
                    os.makedirs(f"{data_dir}/review_gallery/{category}")


                # Limit the number of photos retrieved from each item. 
                showcase_number = 3
                review_number = 5


                # Take couple of first and lasts photos to increase probability of get various angles.
                showcase_images_links = showcase_images_links[:showcase_number] + showcase_images_links[-3:]


                # Randomize photo order to prevent same-sender grouping.
                if len(review_image_links) > review_number:
                    random.shuffle(review_image_links)
                    review_image_links = review_image_links[:review_number]


                for src in showcase_images_links + review_image_links:
                    image_type = ("review_gallery" if src in review_image_links else "showcase")
                    src_path = f"{data_dir}/{image_type}/{category}"


                    # Map thumbnail URLs to full-resolution image URLs.
                    if image_type == "review_gallery":
                        src = src[: src.rfind("/")] + "/fs.webp"
                    else:
                        index = src.find("images")
                        rplc = src[index + src[index:].find("/") + 1 : src.rfind("/")]
                        src = src.replace(rplc, "big")


                    # Verify if photo wasn't previously downloaded.
                    if os.path.exists(f"logs/{category}_{image_type}_stats_log.txt"):
                        with open(
                            f"logs/{category}_{image_type}_stats_log.txt", "r"
                        ) as handler:
                            if src in [str.split()[1] for str in handler.readlines()]:
                                continue


                    # Get count of images of photo by it's ID.
                    files_for_item = [
                        f for f in os.listdir(src_path)
                        if f.startswith(f"{item_id}_") and f.split("_")[-1].split(".")[0].isdigit()
                    ]
                    if files_for_item:
                        i = max(int(f.split("_")[-1].split(".")[0]) for f in files_for_item) + 1
                    else:
                        i = 0


                    # Form filename if {item id}_{number of items photos}.{exstension} format.
                    extension_index = src.rfind(".")
                    filename = f"{src_path}/{item_id}_sample_{i}.{src[extension_index + 1:]}"


                    # Download image.
                    img_data = requests.get(src).content
                    with open(filename, "wb") as handler:
                        handler.write(img_data)


                    # Write image link to downloaded list.
                    with open(
                        f"logs/{category}_{image_type}_stats.txt", "a"
                    ) as handler:
                        handler.write(f"{i} {src}\n")


        # Generate file with stats.
        helpers.counter.generate_stats_file("logs/stats.log")


    def parse_all(self):
        """With specified list use parser method to get exact data from the links. Use only page-logic."""
        try:
            parsing_list = [
                "https://www.wildberries.ru/brands/1836-finn-flare/all",
                "https://www.wildberries.ru/brands/befree/all",
                "https://www.wildberries.ru/brands/mango/all",
                "https://www.wildberries.ru/brands/7049-mark-formelle/all",
                "https://www.wildberries.ru/brands/290923899-maag/all",
                "https://www.wildberries.ru/brands/zarina/all",
                "https://www.wildberries.ru/brands/baon/all",
                "https://www.wildberries.ru/brands/sela/all",
            ]
            parsing_list_with_odezdha = [
                "https://www.wildberries.ru/brands/1092023-mabag-eco/odezhda/",
                "https://www.wildberries.ru/brands/love-republic/odezhda/",
                "https://www.wildberries.ru/brands/urban-tiger/odezhda/",
                "https://www.wildberries.ru/brands/elis-24907/odezhda/",
                "https://www.wildberries.ru/brands/ivolga/odezhda/",
                "https://www.wildberries.ru/brands/mollis/odezhda/",
                "https://www.wildberries.ru/brands/ostin/odezhda/",
                "https://www.wildberries.ru/brands/pompa/odezhda/",
                "https://www.wildberries.ru/brands/emka/odezhda/",
            ]


            # Log info.
            if not os.path.isdir("logs"):
                os.mkdir("logs")
            start_time = datetime.now()
            with open("logs/actions.log", "a") as file:
                file.write(f"Parsing started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")


            for link in parsing_list + parsing_list_with_odezdha:

                for i in range(1, 4):
                    self.browser.get(f"{link}?sort=popular&page={i}")

                    self.wait.until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "product-card__wrapper")
                        )
                    )

                    start = self.browser.find_element(By.CLASS_NAME, "catalog-title-wrap")
                    end = self.browser.find_element(By.TAG_NAME, "footer")

                    for _ in range(5):
                        self.actions.move_to_element(end).perform()
                        self.actions.move_to_element(start).perform()

                    page_catalog = [
                        link.get_attribute("href")
                        for link in self.browser.find_elements(
                            By.XPATH, '//a[contains(@class, "product-card__link")]'
                        )
                    ]

                    # Avoid processing small shops.
                    if len(page_catalog) < 80:
                        break

                    self._parse_process(page_catalog)

            self.browser.quit()
            
        # Except premature ending.
        finally:
            end_time = datetime.now()
            duration = end_time - start_time
            with open("logs/actions.log", "a") as file:
                file.write(f"Premature end: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Duration: {duration}\n\n")

