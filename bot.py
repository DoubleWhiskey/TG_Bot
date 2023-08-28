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
    kick = types.KeyboardButton('Удар!')
    hug = types.KeyboardButton('Обнимашки!')
    markup.add(kick, hug)
    bot.send_message(message.chat.id, 'Привет')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALWxmTnBU8qge-uoBMFtAvw10YamWIkAAK2CQACeVziCcZOco3KlyVIMAQ')
    bot.send_message(message.chat.id, 'Хочешь кого-нибудь ударить или обнять?', reply_markup=markup)


@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.reply_to(message, text)


users_list = ['ТайныйКраб', 'ToribezB', 'Belkakel', 'K_tsx', 'Vasili', 'Keks9tina', 'Bilk123']


def kick_ass(kicker):
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


def hug_func(hugger):
    victim = choice(list(filter(lambda x: x != hugger, users_list)))
    amount = randint(1, 666)
    if amount % 10 == 1 and amount % 100 != 11:
        flower = 'цветочек'
    elif amount % 10 in (2, 3, 4) and str(amount)[-2] != '1':
        flower = 'цветочка'
    else:
        flower = 'цветочков'

    hugger_gender = 'обняла' if hugger in ('ToribezB', 'Belkakel') else 'обнял'
    victim_gender = 'ей' if victim in ('ToribezB', 'Belkakel') else 'ему'
    result = 'подарила' if hugger in ('ToribezB', 'Belkakel') else 'подарил'

    return f"{hugger} {hugger_gender} @{victim} и {result} {victim_gender} {amount} {flower}!"


@bot.message_handler(content_types=['text'])
def echo(message):
    answers_dict = {
        'Привет': 'прив, чё делал?',
        'Как дела?': 'норм',
        'Удар!': kick_ass(message.from_user.username or message.from_user.first_name),
        'Обнимашки!': hug_func(message.from_user.username or message.from_user.first_name),

    }
    answer = answers_dict.get(message.text)
    if answer:
        bot.send_message(message.chat.id, answer)
    else:
        # bot.send_message(message.chat.id, message.text)
        pass


bot.infinity_polling()
