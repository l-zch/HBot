from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from os import system
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from sys import platform


if platform == 'win32': 
    system_commands = ["start chrome --remote-debugging-port=9222",
              ChromeDriverManager().install(),
              "start chrome https://nhentai.net",
              "taskkill /F /IM chrome* /T"],
elif platform == 'linux':
    system_commands =  ["chromium-browser --disable-infobars --disable-gpu --remote-debugging-port=9222 'https://nhentai.net' &",
              "/usr/lib/chromium-browser/chromedriver",
              "chromium-browser 'https://nhentai.net'",
              "killall chromium-browse"]


class WebDriver:
    driver = None

    @classmethod
    def create_driver(cls):
        
        system(system_commands[0])

        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        cls.driver = webdriver.Chrome(system_commands[1], options=options, keep_alive=True)

    @staticmethod
    def _solve_challenge():
        system(system_commands[2])
        sleep(6)

    @classmethod
    def get_soup(cls, url) -> BeautifulSoup:
        try:
            cls.driver.get(url)
        except:
            system(system_commands[3])
            cls.create_driver()
            cls.driver.get(url)
        soup = BeautifulSoup(cls.driver.page_source, "html.parser")

        if soup.find("title").text == "Just a moment...":
            print("bruh")
            cls._solve_challenge()
            soup = cls.get_soup()
        return soup
