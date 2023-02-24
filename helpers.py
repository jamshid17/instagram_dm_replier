from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


def setup_driver(profile_folder):
    fire_options = Options()
    fire_options.profile = profile_folder
    # fire_options.headless = True
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=fire_options)
    driver.maximize_window() 
    action = ActionChains(driver=driver)

    return driver, action
