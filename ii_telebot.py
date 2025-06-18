from io import BytesIO

import telebot
from dotenv import dotenv_values

from calendar_script import get_today_request, get_today_holidays
from kandinsky_script import get_pic_for_today

config = dotenv_values(".env")

bot = telebot.TeleBot(config.get('TOKEN_BOT'), parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 'Чтобы отпраздновать сегодняшний праздник, отправь команду /ii.  \n\nЧтобы сгенерировать еическую картинку, отправь команду /iii. \n\nЧтобы получить список праздников на сегодня, отправь /holidays')


@bot.message_handler(commands=['ii'])
def send_img(message):
    if message.from_user.username in ('AnnaTityushina', 'languidPhonetician'):
        req = get_today_request()
        bot.reply_to(message, f"Надо подождать. Сегодня празднуем: {req}")
        try:
            image_data = get_pic_for_today(req)
            image_file = BytesIO(image_data)
            image_file.name = 'image.png'
            bot.send_photo(message.chat.id, image_file)
        except Exception as e:
            bot.reply_to(message, f"Error sending image: {e}")

    else:
        bot.reply_to(message,
                     "А вы кто")


@bot.message_handler(commands=['iii'])
def send_img(message):
    if message.from_user.username in ('AnnaTityushina', 'languidPhonetician'):
        bot.reply_to(message, f"Надо подождать. Всё будет еически.")
        try:
            image_data = get_pic_for_today('еическое')
            image_file = BytesIO(image_data)
            image_file.name = 'image.png'
            bot.send_photo(message.chat.id, image_file)
        except Exception as e:
            bot.reply_to(message, f"Error sending image: {e}")

    else:
        bot.reply_to(message,
                     "А вы кто")


@bot.message_handler(commands=['holidays'])
def send_img(message):
    if message.from_user.username in ('AnnaTityushina', 'languidPhonetician'):
        holidays = get_today_holidays()
        bot.reply_to(message, f"Сегодня празднуем:\n\n {holidays}")
    else:
        bot.reply_to(message,
                     "А вы кто")


def launch_bot():
    print("The code bot is launched")
    bot.infinity_polling()


launch_bot()
