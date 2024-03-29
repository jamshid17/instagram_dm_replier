import telebot
import environ
from config import *
from ig_bot import check_dm
from .helpers import markdown_escaper

#reading environ
env = environ.Env(
    TELEGRAM_BOT_KEY=(str, ''),
    USER_ID=(int, 0000),
)
environ.Env.read_env()
BOT_KEY = env('TELEGRAM_BOT_KEY')
ONLY_USER_ID = env('USER_ID')

#starting bot
bot = telebot.TeleBot(BOT_KEY)

@bot.message_handler(commands=['start'])
def handle_command_start(message):
    bot.send_message(chat_id=message.chat.id, text=default_text)


@bot.message_handler(commands=['check_instagram'])
def handle_command_start(message):
    user_id = message.from_user.id
    if user_id == ONLY_USER_ID:
        checking_message = bot.send_message(chat_id=message.chat.id, text=checking_dm_message)
        dm_results = check_dm()
        if dm_results == {}:
            overall_text = zero_messages_text
        else:
            overall_text = you_have_messages_text.format(len(dm_results['names'])) + ':\n\n'
            for sender_name, sender_message_types, sender_message_texts in zip(dm_results['names'], dm_results['types'], dm_results['texts']):
                sender_text = f"_{sender_name}_:\n"
                for message_type, message_text in zip(sender_message_types, sender_message_texts):
                    sender_text += markdown_escaper(f"{message_type}:  {message_text}\n")
                sender_text = sender_text[:-1]

                overall_text += sender_text + '\n\n'
            overall_text = overall_text[:-1]
        print(overall_text, "\noverall_text")
        bot.send_message(
            chat_id=message.chat.id, 
            text=overall_text, 
            reply_to_message_id=checking_message.message_id, 
            parse_mode='MarkdownV2'
            )
    else:
        bot.send_message(
            chat_id=message.chat.id, 
            text=dont_know_you_text, 
            parse_mode='MarkdownV2'
            )
bot.infinity_polling()
