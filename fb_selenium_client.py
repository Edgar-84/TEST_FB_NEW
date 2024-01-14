import random

from selenium.webdriver.support.wait import WebDriverWait

from logger_settings import logger
from base_selenium_module import BaseSeleniumDriver

import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class FaceBookButtons:
    POST_ELEMENT_IN_GROUP = '//*[@class="x1cy8zhl x78zum5 x1q0g3np xod5an3 x1pi30zi x1swvt13 xz9dl7a"]'
    COUNT_LIKES_BUTTON = '//*[@class="xrbpyxo x6ikm8r x10wlt62 xlyipyv x1exxlbk"]'


class FaceBookClient(BaseSeleniumDriver, FaceBookButtons):
    def __init__(self,
                 username: str,
                 password: str,
                 hidden: bool,
                 driver_path: str,
                 chrome_location_path: str = None,
                 implicitly_wait: int = None,
                 options: Options = None) -> None:
        self._fb_url = 'https://www.facebook.com/'
        self._username = username
        self._password = password

        if options is None:
            options = webdriver.ChromeOptions()

        if hidden:
            options.add_argument('--headless=new')

        options.add_argument("--disable-popup-window")
        options.add_argument('disable-notifications')

        if chrome_location_path:
            logger.info('Set chrome local')
            options.binary_location = chrome_location_path
            host = "127.0.0.1:9015"
            options.add_experimental_option("debuggerAddress", host)
            options.add_argument("disable-notifications")
            options.add_argument("--app-shell-host-no-handlers")
            self.driver = webdriver.Chrome(options=options, service=Service(driver_path))
            print('Ready Chrome options')

        options.add_argument('--proxy-server=162.223.94.164:80')

        super().__init__(chrome_driver_path=driver_path, options=options, implicitly_wait_time=implicitly_wait)
        logger.info("Driver For FB Ready")

    def while_not_xpath(self, xpath: str, wait: int = 3) -> bool:
        count = 0
        while True:
            if count == wait:
                return False

            if self.xpath_exist(xpath):
                return True
            else:
                count += 1
                time.sleep(count)

    def login_facebook(self) -> bool:
        browser = self.driver
        browser.get(self._fb_url)
        time.sleep(4)

        email_input = self.driver.find_element(By.XPATH, '//*[@id="email"]')
        if email_input:
            email_input.clear()
            email_input.send_keys(self._username)
            time.sleep(3)

            password_input = self.driver.find_element(By.XPATH, '//*[@id="pass"]')
            if password_input:
                password_input.clear()
                password_input.send_keys(self._password)
                password_input.send_keys(Keys.ENTER)

                self.while_not_xpath('//*[@aria-label="Friends"]', wait=5)
                if self.driver.find_element(By.XPATH, '//*[@aria-label="Friends"]'):
                    return True

        return False

    def save_html_page_users_who_likes_post(self, name_file: str):
        try:
            if self.while_not_xpath(self.COUNT_LIKES_BUTTON, wait=5) is False:
                logger.warning(f"Didn't find count_likes on page")
                return False

            like_posts = self.driver.find_elements(By.XPATH, self.COUNT_LIKES_BUTTON)
            count_like_posts = int(like_posts[0].text)
            logger.info(f"Count Likes: {count_like_posts}")
            like_posts[0].click()

            all_button_xpath = f'//*[@aria-label="All, {count_like_posts}"]'
            if self.while_not_xpath(all_button_xpath) is False:
                logger.warning(f"Didn't find button 'All liked persons'")
                return False

            self.driver.find_element(By.XPATH, all_button_xpath).click()

            i = 1
            while True:
                try:
                    scrol_xpath = f'(//div[@data-visualcompletion="ignore-dynamic" and not (@role) and not (@class )])[{i}]'
                    if self.while_not_xpath(scrol_xpath, wait=5) is False:
                        raise Exception('End scrolls')
                    row = self.driver.find_element(By.XPATH, scrol_xpath)
                    time.sleep(random.randrange(1, 2))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
                    i += 1

                except Exception as ex:
                    logger.warning(ex)
                    logger.info('Scrolled all the element, and must have not found the index hence break from the loop')
                    break

            self.save_current_page(name_file)
            return True

        except Exception as ex:
            logger.error(f'Mistake during Save_page_users_who_likes_post: {ex}')
            return False

    def save_html_page_with_all_posts(self, name_file: str):
        try:
            all_links = []
            page_height = self.driver.execute_script('return document.documentElement.scrollHeight')
            iteration = 1
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            logger.info(f"Last night: {last_height}")
            while True:
                if iteration == 20:
                    break
                # self.driver.execute_script(f"window.scrollTo(0, {last_height})")
                # self.driver.execute_script("window.scrollBy(0, arguments[0]);", 600)

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # document.documentElement.scrollHeight)
                time.sleep(random.randrange(5, 8))
                # scroll_pix = random.randrange(10, 30)
                # self.driver.execute_script(f"window.scrollTo(0, -{scroll_pix})")
                self.driver.execute_script('window.scrollBy(0, -300);')
                time.sleep(random.randrange(3, 5))

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                logger.info(f'New height {new_height}')

                #________________________________________

                page_data = self.driver.page_source
                logger.info(f"Page data len {len(page_data)}")

                with open(name_file, 'w', encoding='utf-8') as file:
                    file.write(page_data)

                posts_links = self.get_all_posts_links(name_file)
                logger.info(f'Posts_links: {len(posts_links)}')
                if posts_links:
                    for link in posts_links:
                        if link not in all_links:
                            logger.info(f'Append new link: {link}')
                            all_links.append(link)



                # ________________________________________
                if new_height == last_height:
                    logger.warning(f"{new_height} == {last_height}")
                    break

                last_height = new_height
                logger.info(f"Finished iteration {iteration} ...")
                iteration += 1

            logger.info('Finished scrolling........................')
            logger.info(f"All_links: len {len(all_links)} {all_links}")
            print(all_links)
            time.sleep(5)
            # with open(name_file, 'w', encoding='utf-8') as file:
            #     file.write(self.driver.page_source)
            # self.save_current_page(name_file)
            return True

        except Exception as ex:
            logger.error(f'Mistake during [save_html_page_with_all_posts]: {ex}')
            time.sleep(5)
            # self.save_current_page(name_file)
            with open(name_file, 'w', encoding='utf-8') as file:
                file.write(self.driver.page_source)
            return False

    @staticmethod
    def get_all_posts_links(path_html: str) -> bool or list:
        # comments_class = ('x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r '
        #                   'x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq '
        #                   'x1a2a7pz xt0b8zv xi81zsa xo1l8bm')

        comment_class = ('x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r '
                         'x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq '
                         'x1a2a7pz xt0b8zv xi81zsa xo1l8bm')

        # class_name = 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z'
        class_to_href = ('x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi '
                         'x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm '
                         'xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg '
                         'xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv '
                         'x1a2a7pz x1lliihq x1pdlv7q')

        class_to_post = 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z'

        try:
            with open(path_html, encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            all_posts = soup.find_all(class_=class_to_href)
            posts_without_photo = soup.find_all(class_=comment_class)

            logger.info(f"Count posts: {len(all_posts)}")
            logger.info(f"Count posts without photo: {len(all_posts)}")
            all_posts_link = []

            logger.info('Getting posts without photo ...')
            for post in all_posts:
                link = post.get('href').split('[0]')[0]
                logger.info(f"Link: {link}")
                all_posts_link.append(link)

            # logger.info('Getting posts without photo ...')
            # for post in posts_without_photo:
            #     link = post.get('href')
            #     logger.info(f"Link: {link}")
            #
            #     all_posts_link.append(link)

            return all_posts_link

        except Exception as ex:
            logger.error(f"Mistake during work [get_all_posts_links]: {ex}")
            return False

    @staticmethod
    def get_all_liked_person_links(path_html: str) -> bool or list:
        try:
            with open(path_html, encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            items_divs = soup.find_all('div', class_="x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq")
            logger.info(f"Get divs {len(items_divs)}")

            all_urls = []

            for item in items_divs:
                item_url = item.find("div", class_='x78zum5 xdt5ytf xq8finb x1xmf6yo x1e56ztr x1n2onr6 xqcrz7y').find('a')
                person_link = item_url.get('href')
                if '/user/' in person_link:
                    link = person_link.split('/user/')[-1].split('/')[0]
                    # logger.info(link)
                    all_urls.append(link)

            logger.info(f"Al URL count: {len(all_urls)} {all_urls}")

            return all_urls

        except Exception as ex:
            logger.error(f"Mistake during work 'get_all_liked_person_links': {ex}")
            return False
