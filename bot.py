import telebot
from config import TOKEN
from telebot import types

from speech_recognition_logic import recognize_speech, download_file

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def say_hi(message):
    # Функция, отправляющая "Привет" в ответ на команду /start
    bot.send_message(message.chat.id, 'Привет')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJfil-7g5saK6caYV8CsqELuWLynDH2AALiBgACOtEHAAFgVDNflxcX6h4E')


@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('РикРолл')
    item2 = types.KeyboardButton('Котики')
    item3 = types.KeyboardButton('Окташа')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def echo(message):
    answers_dict = {
        'РикРолл': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'Котики': 'https://www.google.com/search?sca_esv=557208691&sxsrf=AB5stBgx_w9XSr8o0tcCx4B8kQqMgT6b7g:1692133800242&q=%D0%BA%D0%BE%D1%82%D0%B8%D0%BA%D0%B8&tbm=isch&source=lnms&sa=X&ved=2ahUKEwi7rM3Qyd-AAxXKxQIHHUqlAbMQ0pQJegQICRAB&biw=1536&bih=739&dpr=1.25',
        'Окташа': 'https://www.google.com/search?sca_esv=557208691&sxsrf=AB5stBiffz1j_bkUhVoNuFG31WN7wXM32Q:1692133862391&q=skoda+octavia+rs&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjd0Z7uyd-AAxXI0AIHHf8wDLEQ0pQJegQIDBAB&biw=1536&bih=739&dpr=1.25',
        'Привет': 'прив, чё делал?',
        'Как дела?': 'норм',
        'Лох': f"А может ты сам лох, {message.chat.first_name}"
    }
    answer = answers_dict.get(message.text)
    if answer:
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, message.text)
        # pass


bot.infinity_polling()
