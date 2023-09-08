import telebot
from config import TOKEN
from telebot import types

from speech_recognition_logic import recognize_speech, download_file
from fight_or_hug_logic import kick_or_hug
from orm_database import add_player, all_players, statistic

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def say_hi(message):
    user = message.from_user.username or message.from_user.first_name
    if user in all_players():
        to_the_business(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        club = types.KeyboardButton('Я в деле!')
        pussy = types.KeyboardButton('Я пуська(')
        markup.add(club, pussy)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAL81mT6_C5Phnx_6qbrm8h3ctGRHtnHAAL9GgACNeKgS3dqE61odyNCMAQ')
        bot.send_message(message.chat.id, f"Привет, {user}! Хочешь вступить в наш клуб?", reply_markup=markup)
        bot.register_next_step_handler(message, add_or_nah)


def add_or_nah(message):
    chat = message.chat.id
    answer = message.text

    if answer == 'Я в деле!':
        user = message.from_user.username or message.from_user.first_name
        bot.send_sticker(chat, 'CAACAgIAAxkBAAL82GT6_E3SRxAY6bqYCoVA3Xs9Al3mAAKmGQACaWehS61jIKeOdobtMAQ')
        bot.send_message(chat, f'Добро пожаловать в клуб!\nНе забывай правила...')
        add_player(user)
        to_the_business(message)

    elif answer == 'Я пуська(':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go_back = types.KeyboardButton('Я передумал(а)!')
        markup.add(go_back)
        bot.send_sticker(chat, 'CAACAgIAAxkBAAL82mT6_I9XB991ig4amZAjx4_OgxwbAAKxGgAC3vWhS-cUzkOLVSQEMAQ')
        bot.send_message(chat, f'Я так и думал. Возвращайся, если передумаешь...', reply_markup=markup)

    else:
        bot.send_message(chat, f'Просто нажми кнопку!')
        bot.register_next_step_handler(message, add_or_nah)


def to_the_business(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kick = types.KeyboardButton('Удар!')
    hug = types.KeyboardButton('Обнимашки!')
    stat = types.KeyboardButton('Статистика.')
    markup.add(kick, hug, stat)
    bot.send_message(message.chat.id, 'Хочешь кого-нибудь ударить или обнять?', reply_markup=markup)


def change_mind(message):
    chat = message.chat.id
    user = message.from_user.username or message.from_user.first_name
    add_player(user)
    bot.send_message(chat, 'Я рад, что ты передумал(а)!\nДобро пожаловать в клуб!\nНе забывай правила...')
    to_the_business(message)


@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def echo(message):
    answers_dict = {
        'Удар!': kick_or_hug('kick', message.from_user.username or message.from_user.first_name),
        'Обнимашки!': kick_or_hug('hug', message.from_user.username or message.from_user.first_name),
        'Статистика.': statistic(message.from_user.username or message.from_user.first_name),
        'Я передумал(а)!': change_mind(message),

    }
    answer = answers_dict.get(message.text)
    if answer:
        bot.send_message(message.chat.id, answer)
    else:
        pass


bot.infinity_polling()
