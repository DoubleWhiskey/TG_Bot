import telebot
from config import TOKEN
from telebot import types
from random import choice, randint

from speech_recognition_logic import recognize_speech, download_file

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def say_hi(message):
    # Функция, отправляющая "Привет" в ответ на команду /start
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Удар!')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALWxmTnBU8qge-uoBMFtAvw10YamWIkAAK2CQACeVziCcZOco3KlyVIMAQ')
    bot.send_message(message.chat.id, 'Хочешь кого-нибудь ударить?', reply_markup=markup)


@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.reply_to(message, text)


def kick_ass(kicker):
    users_list = ['ТайныйКраб', 'ToribezB', 'Belkakel', 'K_tsx', 'Vasili', 'Keks9tina', 'Bilk123']

    victim = choice(list(filter(lambda x: x != kicker, users_list)))
    amount = randint(1, 32)
    if amount in (1, 21, 31):
        teeth = 'зуб'
    elif amount % 10 in (2, 3, 4) and str(amount)[0] != '1':
        teeth = 'зуба'
    else:
        teeth = 'зубов'

    kicker_gender = 'ударила' if kicker in ('ToribezB', 'Belkakel') else 'ударил'
    victim_gender = 'ей' if victim in ('ToribezB', 'Belkakel') else 'ему'
    result = 'выбила' if kicker in ('ToribezB', 'Belkakel') else 'выбил'

    return f"{kicker} {kicker_gender} @{victim} и {result} {victim_gender} {amount} {teeth}!"


@bot.message_handler(content_types=['text'])
def echo(message):
    answers_dict = {
        'Привет': 'прив, чё делал?',
        'Как дела?': 'норм',
        'Удар!': kick_ass(message.from_user.username or message.from_user.first_name),

    }
    answer = answers_dict.get(message.text)
    if answer:
        bot.send_message(message.chat.id, answer)
    else:
        # bot.send_message(message.chat.id, message.text)
        pass


bot.infinity_polling()
