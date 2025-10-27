"""Wildberries class-parser

Parse photos from comments and gallery sections of most popular positions from certain shops listed in the code. 
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import requests
import random
import os


showcase_count = 5
review_count = 5

class WildberriesParser:
    def __init__(self):
        """Initializes a browser instance.

        The options should include built-in optimization with an initialized browser.
        They should also specify the list of categories allowed for parsing.
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


        self.categories = {
            "Blouse": ["Блузка", "Блузка-боди"],
            "Cape": ["Плащ", "Тренчкот"],
            "Cardigan": ["Водолазка", "Термоводолазка", "Джемпер", "Кардиган", "Джемпер спортивный", "Пуловер", "Свитшот"],
            "Coat": ["Пальто", "Полупальто"],
            "Dress": ["Платье", "Сарафан", "Платье спортивное", "Туника"],
            "Gloves": ["Перчатки", "Варежки", "Митенки"],
            "Hat": ["Балаклава", "Бейсболка", "Панама", "Кепи", "Шапка", "Шапка-ушанка", "Шляпа", "Шапка-шлем", "Козырек", "Берет"],
            "Jacket": ["Анорак", "Бомбер", "Жакет", "Куртка", "Пиджак", "Куртка спортивная", "Ветровка", "Косуха"],
            "Jumpsuit": ["Комбинезон", "Полукомбинезон"],
            "Longsleeve": ["Лонгслив", "Рашгард", "Лонгслив спортивный", "Термолонгслив"],
            "Pants": ["Бриджи", "Бриджи спортивные", "Брюки", "Брюки спортивные", "Велосипедки", "Джеггинсы", "Джинсы", "Леггинсы", "Тайтсы", "Капри"],
            "Scarf": ["Платок", "Палантин", "Шарф", "Снуд"],
            "Shirt": ["Рубашки"],
            "Shorts": ["Бордшорты", "Шорты", "Шорты спортивные", "Бермуды"],
            "Skirt": ["Юбка спортивная", "Юбка"],
            "Sweater": ["Свитер", "Кофта"],
            "Sweatshirt": ["Толстовка", "Толстовка спортивная", "Худи"],
            "T-shirt, Polo": ["Футболки", "Футболка спортивная", "Футболка-поло", "Термофутболка", "Майка спортивная", "Манишка"],
            "Top": ["Топ"],
            "Underwear": ["Боди", "Кальсоны", "Комплект белья", "Леггинсы ч/н", "Майка бельевая", "Неглиже", "Ночная сорочка", "Пижама", "Плавки", "Термободи", "Трусы", "Кальсоны спортивные", "Корсет", "Пеньюар"],
            "Vest": ["Жилеты"],
            "Winter Jacket": ["Пуховик", "Дубленка", "Парка", "Шуба искусственная"],
            "Belt": ["Ремень", "Пояс"],
            "Shoes": ["Босоножки", "Сандалии", "Сабо", "Полусапожки", "Мокасины", "Лоферы", "Балетки", "Кеды", "Туфли", "Ботинки", "Полуботинки", "Мюли", "Кроссовки", "Ледоступы", "Резиновые сапоги", "Сапоги", "Ботильоны", "Угги", "Ботфорты", "Дутики"],
            "Stockings": ["Гольфы", "Колготки", "Термоколготки", "Гетры"]
#            "Bag": ["Рюкзак", "Сумка", "Сумка-шоппер", "Сумка спортивная"]
#            "Bra": ["Бюстгальтер", "Лиф для купальника", "Топ спортивный"],
#            "Socks": ["Носки", "Подследники", "Термоноски"],
#            "Sunglasses": ["Солнцезащитные очки"],
        }

    def get_category(self, item_name):
        """Method to check if the category needs to be parsed."""
        item_name = item_name.lower()

        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in item_name:
                    return category

        return "None"

    def parse_all(self):
        """With specified list use parser method to get exact data from the links. Use only page-logic."""
        parsing_list = ["https://www.wildberries.ru/brands/7049-mark-formelle/all",
                        "https://www.wildberries.ru/brands/1836-finn-flare/all",
                        "https://www.wildberries.ru/brands/290923899-maag/all",
                        "https://www.wildberries.ru/brands/gloria-jeans/all",
                        "https://www.wildberries.ru/brands/zarina/all",
                        "https://www.wildberries.ru/brands/befree/all",
                        "https://www.wildberries.ru/brands/mango/all",
                        "https://www.wildberries.ru/brands/baon/all",
                        "https://www.wildberries.ru/brands/sela/all"
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
                
                if len(page_catalog) < 80:
                    break
                    
                self.__parse_wildberries(page_catalog)

        self.browser.quit()

    def __parse_wildberries(self, page_catalog):
        """From selected page method gets photos from both of gallery and comments sections."""
        cur_dir = "data/wildberries"

        if not os.path.isdir(f"{cur_dir}/showcase"):
            os.makedirs(f"{cur_dir}/showcase")
        if not os.path.isdir(f"{cur_dir}/review_gallery"):
            os.makedirs(f"{cur_dir}/review_gallery")
        if not os.path.isdir("logs"):
            os.mkdir("logs")

        for item in page_catalog:
            self.browser.get(item)

            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//span[contains(@class, "categoryLinkCategory--VSJ8c")]')
            ))

            category_elem = self.browser.find_element(
                By.XPATH, '//span[contains(@class, "categoryLinkCategory--VSJ8c")]'
            )

            category = category_elem.get_attribute("innerHTML")
            print(f"{category}")

            category = self.get_category(category)

            print(f"{category}")

            if category == "None":
                continue

            item_id = item[item.find("catalog") + len("catalog") + 1 : item.rfind("/")]

            print(f"{item_id}")


            showcase_classes = self.browser.find_elements(
                By.XPATH, '//div[contains(@class, "swiper-slide miniatureSlide--acvJc")]')[:showcase_count]
            showcase_images_links = [elem.find_element(
                By.TAG_NAME, 'img').get_attribute('src') for elem in showcase_classes]

            actions = ActionChains(self.browser)

            end = self.browser.find_element(
                By.ID, 'product-feedbacks')

            actions.move_to_element(end).perform()


            review_classes = self.browser.find_elements(
                By.XPATH, '//img[contains(@class, "image--CJ2Ug")]')

            review_image_links = [elem.get_attribute('src') for elem in review_classes]

            print(len(review_image_links), len(showcase_images_links))
            print(len(set(review_image_links)), len(set(showcase_images_links)))

            if len(review_image_links) and len(showcase_images_links):

                if len(review_image_links) > review_count:
                    random.shuffle(review_image_links)
                    review_image_links = review_image_links[:review_count]

                if not os.path.isdir(f"{cur_dir}/showcase/{category}"):
                    os.makedirs(f"{cur_dir}/showcase/{category}")

                if not os.path.isdir(f"{cur_dir}/review_gallery/{category}"):
                    os.makedirs(f"{cur_dir}/review_gallery/{category}")


                for src in (showcase_images_links + review_image_links):

                    image_type = "review_gallery" if src in review_image_links else "showcase"
                    
                    if image_type == "review_gallery":
                        src = src[:src.rfind('/')] + "/fs.webp"
                    else:
                        index = src.find("images")
                        rplc = src[index +
                                src[index:].find('/') + 1: src.rfind('/')]
                        src = src.replace(rplc, "big")

                    if os.path.exists(f"logs/{category}_{image_type}_stats_log.txt"):
                        with open(f"logs/{category}_{image_type}_stats_log.txt", 'r') as handler:
                            if src in [str.split()[1] for str in handler.readlines()]:
                                continue

                    i = 0 
                    if len([filename for filename in os.listdir(f"{cur_dir}/{image_type}/{category}") if filename.split('_')[-1].split('.')[0].isdigit()]) > 0: 
                        i = max([int(el.split('_')[-1].split('.')[0]) for el in os.listdir(
                            f"{cur_dir}/{image_type}/{category}") if el.split('_')[-1].split('.')[0].isdigit()])

                    extension_index = src.rfind('.')
                    filename = f"{cur_dir}/{image_type}/{category}/{item_id}_sample_{i + 1}.{src[extension_index + 1:]}"

                    img_data = requests.get(src).content

                    with open(filename, 'wb') as handler:
                        handler.write(img_data)

                    with open("logs/stats.log", 'w') as file:
                        stats = [f"{r} - {len(files)}\n" for r,
                                _, files in os.walk(f"./{cur_dir}")]
                        review_number = sum(
                            [int(st.split()[-1]) if st.find("review_gallery") != -1 else 0 for st in stats])
                        showcase_number = sum(
                            [int(st.split()[-1]) if st.find("showcase") != -1 else 0 for st in stats])
                        stats.append(f"review all - {review_number}\n")
                        stats.append(f"showcase all - {showcase_number}\n")
                        file.writelines(stats[1:])

                    with open(f"logs/{category}_{image_type}_stats_log.txt", 'a') as handler:
                        handler.write(f"{i} {src}\n")


a = WildberriesParser()
a.parse_all()
