from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from config import *
import environ
from helpers import setup_driver, like_possibility


env = environ.Env()
environ.Env.read_env()
BROWSER_PROFILE = env('BROWSER_PROFILE')



def check_dm():
    return_dict = {}
    driver, action = setup_driver(profile_folder=BROWSER_PROFILE)
    #getting main page
    driver.get('https://www.instagram.com')
    time.sleep(5)
    #disabling turn on/off notification pop-up in case it got out
    try:
        not_now_button = driver.find_element(By.XPATH, f"//button[contains(text(), 'Not Now')]")
        not_now_button.click()
    except:
        pass 
    #pushing the notification bell
    notification_btn = driver.find_element(
        By.XPATH, "//a[contains(@href, '/direct/inbox/')]"
        )
    notification_number_icons = notification_btn.find_elements(
        By.XPATH, f".//div[@class='{notification_number_icon}']"
        )

    if len(notification_number_icons):
        notification_btn.click()
        time.sleep(5)
        #chat_rooms 
        message_rooms = driver.find_elements(
            By.XPATH, f"//div[@class='{message_rooms_class}']"
            )
        all_messager_names = []
        all_message_types = []
        all_message_texts = []
        for message_room in message_rooms:
            #looping through chat rooms. If there is new notification element, we enter to the chat room 
            new_notifications = message_room.find_elements(
                By.XPATH, f".//div[@class='{new_notification_class}']"
                )
            if len(new_notifications) != 0:
                message_types = []
                message_texts = []
                messager_name = message_room.find_element(
                    By.XPATH, f".//div[@class='{messager_name_class}']"
                    ).text
                message_room.click()
                time.sleep(5)
                #reversing messages, so that the latest message will be the first one in the list
                message_elems = driver.find_elements(By.XPATH, f"//div[@class='{message_class}']")
                message_elems.reverse()
                #scrolling to the bottom, just in case 
                helper_elem = message_elems[0].find_element(By.XPATH, ".//a")
                helper_elem.send_keys(Keys.END)
                for message_elem in message_elems:
                    #checking if message is received, not sent
                    own_message_divs = message_elem.find_elements(
                        By.XPATH, f".//div[@class='{own_message_div_class}']"
                    )
                    if len(own_message_divs) == 0:
                        #looping through message elements, if there is reaction, we break the for  loop
                        message_reactions = message_elem.find_elements(
                            By.XPATH, f".//div[@class='{reaction_elem}']"
                            )
                        if len(message_reactions) == 0:

                            print('no reaction')
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
                                        action.double_click(tapable_section).perform()
                                        time.sleep(3)
                                    #adding to messages texts to  result dictinoary 
                                    message_text = author_name
                                    message_type = 'reel'
                                    message_texts.append(message_text)
                                    message_types.append(message_type)                               
                            else: 

                                message_type = None
                                story_headers = message_elem.find_elements(
                                    By.XPATH, f".//h1[@class='{story_header}']"
                                    )
                                image_message_elems = message_elem.find_elements(
                                    By.XPATH, f".//div[@class='{img_class}']"
                                    )
                                gif_message_elems = message_elem.find_elements(
                                    By.XPATH, f".//div[@class='{gif_class}']"
                                    )
                                emoji_message_elems = message_elem.find_elements(
                                    By.XPATH, f".//div[@class='{emoji_class}']"
                                    )
                                audio_message_elems = message_elem.find_elements(
                                    By.XPATH, f".//div[@class='{audio_class}']"
                                    )
                                #collecting messages
                                if len(story_headers) != 0:
                                    message_type = 'story' 
                                elif len(image_message_elems) != 0:
                                    message_type = 'image'
                                elif len(gif_message_elems) != 0:
                                    message_type = 'gif'
                                elif len(emoji_message_elems) != 0:
                                    message_type = 'emoji'
                                elif len(audio_message_elems) != 0:
                                    message_type = 'audio'
                                else:
                                    message_type = 'text'
                                if "to see this type of message." in message_elem.text:
                                    message_text = 'Wrong type of message'
                                else:
                                    message_text = message_elem.text
                                message_texts.append(message_text)
                                message_types.append(message_type)
                                #liking the message if it is the first one
                                if message_elems.index(message_elem) == 0:
                                    if len(story_headers) != 0:
                                        tapable_section = story_headers[0]
                                    else:
                                        tapable_section = message_elem.find_element(
                                            By.XPATH, ".//div[@class=' _ac1n']"
                                            )
                                    action.double_click(tapable_section).perform()
                                    time.sleep(2)
                        else:
                            break
                    else:
                        #if selenium reaches owner's message, break
                        break
                all_messager_names.append(messager_name)
                all_message_types.append(message_types)
                all_message_texts.append(message_texts)
        
        all_messager_names.reverse()
        all_message_types.reverse()
        all_message_texts.reverse()

        return_dict = {
            'names': all_messager_names,
            'types': all_message_types,
            'texts': all_message_texts,
        } 
    
    return return_dict

