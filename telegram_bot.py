from email import charset
from subprocess import call
import telebot
from telebot import types
import environ
from config import *
from extra_functions import *

#reading environ
env = environ.Env()
environ.Env.read_env()

BOT_KEY = env('TELEGRAM_BOT_KEY')

bot = telebot.TeleBot(BOT_KEY)

def make_inline_keyboard(list_of_items):
    markup_lst = []
    for key, value in list_of_items.items():
        markup_lst.append(types.InlineKeyboardButton(text=value, callback_data=key))
    markup = types.InlineKeyboardMarkup(markup_lst)
    return markup

def send_username(user_data):
    bot.send_message(chat_id=user_data['tm_id'], text=send_username_text)

def send_password(user_data):
    bot.send_message(chat_id=user_data['tm_id'], text=send_password_text)

def is_correct(user_data):
    bot.send_message(chat_id=user_data['tm_id'], 
        text=is_correct_text.format(user_data['ig_username'], user_data['ig_password']), 
        reply_markup=make_inline_keyboard({'correct':'Ha', 'incorrect':"Yo'q"}))

def inserting_finished(user_data):
    bot.send_message(chat_id=user_data['tm_id'], text=inserting_done_text)

def send_default_message(user_data):
    bot.send_message(chat_id=user_data['tm_id'], text=default_text)

def wrong_type_of_message(chat_id, key):
    bot.send_message(chat_id=chat_id, text=wrong_type_of_message.format(key))

@bot.message_handler(commands=['start'])
def handle_command_start(message):
    user_data = get_user_data(message=message)
    if user_data['step'] == 'username':
        return send_username(user_data)
    elif user_data['step'] == 'password':
        return send_password(user_data)
    elif user_data['step'] == 'is_correct':
        return is_correct(user_data)
    else:
        return send_default_message(user_data)

@bot.callback_query_handler(func=lambda call: True)
def handle_correct(call):
    user_data = get_user_data(call=call)
    if call.data == 'correct':
        update_dict = { 
            'step':'default',
        }
        update_user_data(update_dict=update_dict, call=call)
        return send_default_message(user_data=user_data)
    elif call.data == 'incorrect':
        update_dict = { 
            'step':'username',
        }
        update_user_data(update_dict=update_dict, call=call)
        return send_username(user_data=user_data)

#MESSAGE AND CALL HANDLERS
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    user_data = get_user_data(message=message)
    if user_data['status'] == 'username':
        ig_username_text = message.text 
        if ' ' in ig_username_text or '\n' in ig_username_text:
            return wrong_type_of_message(chat_id=user_data['user_id'], key='Username')
        else:
            update_dict = {
                'ig_username':ig_username_text, 
                'step':'password',
            }
            update_user_data(update_dict=update_dict, message=message)
            return send_password(user_data=user_data)
    elif user_data['status'] == 'password':
        ig_password_text = message.text 
        if ' ' in ig_password_text or '\n' in ig_password_text:
            return wrong_type_of_message(chat_id=user_data['user_id'], key='Password')
        else:
            update_dict = {
                'ig_password':ig_password_text, 
                'step':'is_correct',
            }
            update_user_data(update_dict=update_dict, message=message)
            return is_correct(user_data=user_data)
    

    # bot.send_message(chat_id=chat_id, 
    #     text=WELCOME_TEXT, reply_markup=make_text_keyboard(LANG_LIST))

bot.infinity_polling()
