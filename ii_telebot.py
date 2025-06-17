from io import BytesIO

import telebot
from dotenv import dotenv_values

from calendar_script import get_today_request
from kandinsky_script import get_pic_for_today

config = dotenv_values(".env")

bot = telebot.TeleBot(config.get('TOKEN_BOT'), parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 'Чтобы сгенерировать еическую картинку, отправь команду /ii')


@bot.message_handler(commands=['ii'])
def send_welcome(message):
    if message.from_user.username in ('AnnaTityushina', 'languidPhonetician'):
        bot.reply_to(message, f"Надо подождать")
        req = get_today_request()
        image_data = get_pic_for_today(req)
        try:
            image_file = BytesIO(image_data)
            image_file.name = 'image.png'
            bot.send_photo(message.chat.id, image_file)
        except Exception as e:
            bot.reply_to(message, f"Error sending image: {e}")

    else:
        bot.reply_to(message,
                     "А вы кто")


def launch_bot():
    print("The code bot is launched")
    bot.infinity_polling()


launch_bot()
