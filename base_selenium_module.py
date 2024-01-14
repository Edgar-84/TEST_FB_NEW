import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from logger_settings import logger
class BaseSeleniumDriver:
    def __init__(self,
                 chrome_driver_path: str,
                 implicitly_wait_time: int = None,
                 options: Options = None,
                 hidden: bool = False) -> None:
        
        if options is None:
            options = Options()

        if hidden:
            options.add_argument('--headless=new')
         
        self.driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        
        if implicitly_wait_time:
            self.driver.implicitly_wait(implicitly_wait_time)

    def close_driver(self):
        self.driver.close()
        self.driver.quit()
    
    def xpath_exist(self, xpath: str) -> bool:
        browser = self.driver
        try:
            browser.find_element(By.XPATH, xpath)
            exist = True

        except NoSuchElementException:
            exist = False

        return exist

    def get_element(self, driver: webdriver, by: By, element: str, wait: int = 3) -> WebElement or None:
        try:
            element = WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((by, element))
            )
            return element
        
        finally:
            return None

    def save_current_page(self, name_save_file: str) -> bool:
        try:
            with open(name_save_file, 'w', encoding='utf-8') as file:
                file.write(self.driver.page_source)
                return True

        except Exception as ex:
            logger.critical(f"Mistake during save page {ex}")
            return False
                