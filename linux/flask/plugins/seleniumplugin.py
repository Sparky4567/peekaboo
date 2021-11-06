from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from config import webdriver_path
from config import selenium_timeout
from config import peek_prefix
from config import peekaboo_agent
from config import eliminate_links
from config import eliminate_tags
import time


class Selenium_Plugin:
    def __init__(self,passed_url):
        self.weboptions = Options()
        self.agent = {"User-Agent":peekaboo_agent}
        self.weboptions.add_argument("user-agent=[{}]".format(self.agent))
        self.weboptions.add_argument("--headless")
        self.weboptions.add_argument("--no-sandbox") 
        self.passed_url = passed_url
        self.prefix = peek_prefix

    def selenium_ini(self):
        driver_path = webdriver_path
        driver = webdriver.Chrome(driver_path,options=self.weboptions)
        driver.get(self.passed_url)
        time.sleep(selenium_timeout)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        for script in soup(eliminate_links):
            script.extract()
        for tag in soup():
            for attribute in eliminate_tags:
                del tag[attribute]
        soup = str(soup).replace('&gt;','>').replace('&lt;','<').replace("'",'"')
        driver.close()
        return soup