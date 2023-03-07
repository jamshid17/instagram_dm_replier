from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import random


def setup_driver(profile_folder):
    fire_options = Options()
    fire_options.profile = profile_folder
    # fire_options.headless = True
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=fire_options)
    driver.maximize_window() 
    action = ActionChains(driver=driver)

    return driver, action


def markdown_escaper(text):
    escaping_chars = [
        '[', ']', '(', ')', '~', 
        '`', '>', '#', '+', '-', 
        '=', '|', '{', '}', '.', 
        '!', '_',
    ]
    for char in escaping_chars:
        text = text.replace(char, '\{}'.format(char))
    return text

def like_possibility():
    rando = random.randint(1, 10)
    x = round(rando/10)
    if x == 1:
        return True
    else:
        return False
