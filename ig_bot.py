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
import environ

def like_possibility():
    rando = random.randint(4, 10)
    x = round(rando/10)
    if x == 1:
        print('yeah')
        return True
    else:
        print('nooo')
        return False

def check_dm():
    #return_dict
    return_dict = {}
    #setting up driver
    fire_options = Options()
    env = environ.Env()
    environ.Env.read_env()
    BROWSER_PROFILE = env('BROWSER_PROFILE')
    fire_options.profile = BROWSER_PROFILE
    # fire_options.headless = True
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=fire_options)
    driver.maximize_window() 
    action = ActionChains(driver=driver)

    driver.get('https://www.instagram.com')
    time.sleep(5)
    #disabling turn on/off notification pop-up in case it got out
    try:
        not_now_button = driver.find_element(By.XPATH, f"//button[contains(text(), 'Not Now')]")
        not_now_button.click()
    except:
        pass 
    #pushing the notification bell
    notification_btn = driver.find_element(By.XPATH, "//a[contains(@href, '/direct/inbox/')]")
    notification_icons = notification_btn.find_elements(By.XPATH, "//div[@class='_aayg']//div[@class='_aadh']")
    if len(notification_icons):
        notification_btn.click()
        time.sleep(10)
        #chat_rooms 
        message_rooms = driver.find_elements(By.XPATH, f"//div[@class='{message_rooms_class}']")
        all_messager_names = []
        all_message_types = []
        all_message_texts = []
        for message_room in message_rooms:
            #looping through chat rooms. If there is new notification element, we enter to the chat room 
            new_notifications = message_room.find_elements(By.XPATH, f".//div[@class='{new_notification_class}']")
            if len(new_notifications) != 0:
                messager_name = message_room.find_element(By.XPATH, f".//div[@class='{messager_name_class}']").text
                all_messager_names.append(messager_name)
                message_room.click()
                time.sleep(15)
                message_types = []
                message_texts = []
                #reversing messages, so that the latest message will be the first one in the list
                message_elems = driver.find_elements(By.XPATH, f"//div[@class='{message_class}']")
                message_elems.reverse()
                #scrolling to the bottom, just in case 
                helper_elem = message_elems[0].find_element(By.XPATH, ".//a")
                helper_elem.send_keys(Keys.END)
                print('send to end')
                for message_elem in message_elems:
                    #looping through message elements, if there is reaction, we break the for  loop
                    message_reactions = message_elem.find_elements(By.XPATH, f".//div[@class='{reaction_elem}']")
                    if len(message_reactions) == 0:
                        first_tapable_sections = message_elem.find_elements(By.XPATH, \
                            f".//div[@class='{shared_post_message_section_class}']")
                        second_tapable_sections = message_elem.find_elements(By.XPATH, \
                            f".//div[@class='{shared_reel_author_name_section_class}']")

                        #if there is tapable section, it is shared post or reel, otherwise, it can be text, 
                        # picture, story or reel without caption (I couldn't find a way to like this type reel). 
                        if len(first_tapable_sections) != 0 or len(second_tapable_sections) != 0:
                            tapable_section = None
                            driver.execute_script("arguments[0].scrollIntoView();", message_elem)
                            if len(first_tapable_sections) != 0:
                                tapable_section = first_tapable_sections[0]
                                author_name = message_elem.find_element(By.XPATH, ".//h1").text
                            elif len(second_tapable_sections) != 0:
                                tapable_section = second_tapable_sections[0]
                                author_name = tapable_section.text
                            if tapable_section:
                                if like_possibility() or message_elems.index(message_elem) == 0:
                                    time.sleep(60)
                                    action.double_click(tapable_section).perform()
                                    time.sleep(3)
                                #adding to messages texts to  result dictinoary 
                                message_text = author_name
                                message_type = 'reel'
                                message_texts.append(message_text)
                                message_types.append(message_type)                               
                        else: 
                            message_type = None
                            story_headers = message_elem.find_elements(By.XPATH, f".//h1[@class='{story_header}']")
                            image_message_elems = message_elem.find_elements(By.XPATH, f".//div[@class='{img_class}']")
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
                            #liking the message if it is the first one
                            if message_elems.index(message_elem) == 0:
                                if len(story_headers) != 0:
                                    tapable_section = story_headers[0]
                                else:
                                    tapable_section = message_elem.find_element(By.XPATH, ".//div[@class='_aa06']")
                                action.double_click(tapable_section).perform()
                                time.sleep(4)
                    else:
                        print('yetib keldik')
                        break
                all_message_types.append(message_types)
                all_message_texts.append(message_texts)
        
        return_dict = {
            'names': all_messager_names,
            'types': all_message_types,
            'texts': all_message_texts,
        } 
    return return_dict

