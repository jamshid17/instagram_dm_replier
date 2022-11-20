from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.firefox import GeckoDriverManager
from config import *
import random 

def like_possibility():
    rando = random.randint(4, 10)
    x = round(rando/10)
    if x == 1:
        return True
    else:
        return False

fire_options = Options()
fire_options.profile = "/Users/user/Library/Application Support/Firefox/Profiles/mp5joo1k.instagram"
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=fire_options)
driver.maximize_window() 
action = ActionChains(driver=driver)

driver.get('https://www.instagram.com')
time.sleep(5)

#pushing the notification bell
notification_btn = driver.find_element(By.XPATH, "//a[contains(@href, '/direct/inbox/')]")
notification_icons = notification_btn.find_elements(By.XPATH, "//div[@class='_aayg']//div[@class='_aadh']")
if len(notification_icons):
    message_num = notification_icons[0].text
    notification_btn.click()
    time.sleep(10)
    new_notifications = driver.find_elements(By.XPATH, f"//div[@class='{new_notification_class}']")
    for new_notification in new_notifications:
        new_notification.click()
        time.sleep(5)
        message_types = []
        message_texts = []
        message_elems = driver.find_elements(By.XPATH, f"//div[@class='{message_class}']")
        message_elems.reverse()
        helper_elem = message_elems[0].find_element(By.XPATH, ".//a")
        for message_elem in message_elems:
            message_reactions = message_elem.find_elements(By.XPATH, f".//div[@class='{reaction_elem}']")
            if len(message_reactions) == 0:
                tapable_sections = message_elem.find_elements(By.XPATH, f".//div[@class='{shared_post_top_section_class}']")
                if len(tapable_sections) != 0:
                    while True:
                        try:
                            action.move_to_element(tapable_sections[0]).perform()
                            actual_tapable_section = message_elem.find_element(By.XPATH, f".//div[@class='{shared_post_message_section_class}']")
                            if like_possibility() or message_elems.index(message_elem) == 0:
                                action.double_click(actual_tapable_section).perform()
                                print('liked hee')      
                                time.sleep(2)
                            else:
                                print('no likey')
                            break
                        except:
                            helper_elem.send_keys(Keys.ARROW_UP) 
                            time.sleep(0.1)
                else: 
                    message_type = None
                    story_headers = message_elem.find_elements(By.XPATH, f".//h1[@class='{story_header}']")
                    image_message_elems = message_elem.find_elements(By.XPATH, f".//div[@class='{img_class}']")
                    if message_elems.index(message_elem) == 0:
                        if len(story_headers) != 0:
                            tapable_section = story_headers[0]
                        else:
                            tapable_section = message_elem.find_element(By.XPATH, ".//div[@class=' _ac1n']")
                        action.double_click(tapable_section).perform()
                        print('liked the first')      
                        time.sleep(2)
                    #collecting messages
                    if len(story_headers) != 0:
                        message_type = 'story' 
                    elif len(image_message_elems) != 0:
                        message_type = 'image'
                    else:
                        message_type = 'text'
                    message_text = message_elem.text
                    message_texts.append(message_text)
                    message_types.append(message_type)
            else:
                print('yetib keldik')
                break
print(message_texts)
print(message_types)
        #     if last_element.is_displayed():
        #         print('yessss')
        #     else:
        #         first_link.send_keys(Keys.ARROW_UP)





        # print('key is sent')
        # for message_elem in message_elems:
        #     print('message gerer')
        #     message_elem.send_keys(Keys.HOME)
        #     time.sleep(5)
            # x_location = message_elem.location['x']
            # y_location = message_elem.location['y']
            # driver.execute_script(f"window.scrollTo({x_location},{y_location}-300);")
            # action.move_to_element(message_elem).perform() 
            # reaction_elems = message_elem.find_elements(By.XPATH, f".//div[@class='{reaction_elem}']")
            # if len(reaction_elems) == 0:
            #     tapable_sections = message_elem.find_elements(By.XPATH, f".//div[@class='{shared_post_message_section_class}']")
            #     if len(tapable_sections) != 0:
            #         action.double_click(tapable_sections[0]).perform()
            #         time.sleep(2)
            #         print('liked hee')
            # else:
            #     break 

