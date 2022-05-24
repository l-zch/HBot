from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from os import system
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchWindowException

class WebDriver:
    driver = None

    @classmethod
    def create_driver(cls):
        system("start chrome --remote-debugging-port=9222")
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        cls.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options, keep_alive=True)

    @staticmethod
    def _solve_challenge():
        system("start chrome https://nhentai.net")
        sleep(6)
    
    @classmethod
    def get_soup(cls, url) -> BeautifulSoup:
        try:
            cls.driver.get(url)
        except:
            cls.create_driver()
            cls.driver.get(url)
        soup = BeautifulSoup(cls.driver.page_source, "html.parser")
        if soup.find("title").text == "Just a moment...":
            print("bruh")
            cls._solve_challenge()
            soup = cls.get_soup()
        return soup

