import telebot
from config import TOKEN
from telebot import types

from speech_recognition_logic import recognize_speech, download_file
from fight_or_hug_logic import kick_or_hug
from orm_database import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def say_hi(message):
    user = message.from_user.username or message.from_user.first_name
    if user in all_players():
        to_the_business(message)
    else:
        add_player(user)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        club = types.KeyboardButton('Я в деле!')
        pussy = types.KeyboardButton('Я пуська(')
        markup.add(club, pussy)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAL81mT6_C5Phnx_6qbrm8h3ctGRHtnHAAL9GgACNeKgS3dqE61odyNCMAQ')
        bot.send_message(message.chat.id, f"Привет, {user}! Хочешь вступить в наш клуб?", reply_markup=markup)
        bot.register_next_step_handler(message, add_or_nah)


def add_or_nah(message):
    # bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    chat = message.chat.id
    answer = message.text
    user = message.from_user.username or message.from_user.first_name

    if answer == 'Я в деле!':
        bot.send_sticker(chat, 'CAACAgIAAxkBAAL82GT6_E3SRxAY6bqYCoVA3Xs9Al3mAAKmGQACaWehS61jIKeOdobtMAQ')
        bot.send_message(chat, f'Добро пожаловать в клуб!\nНе забывай правила...')
        to_the_business(message)

    elif answer == 'Я пуська(':
        i_am_out(chat, user)
        # del_player(user)
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # go_back = types.KeyboardButton('/start')
        # markup.add(go_back)
        # bot.send_sticker(chat, 'CAACAgIAAxkBAAL82mT6_I9XB991ig4amZAjx4_OgxwbAAKxGgAC3vWhS-cUzkOLVSQEMAQ')
        # bot.send_message(chat, f'Я так и думал. Возвращайся, если передумаешь...', reply_markup=markup)

    else:
        bot.send_message(chat, f'Просто нажми кнопку!')
        bot.register_next_step_handler(message, add_or_nah)


def i_am_out(chat, _player_):
    del_player(_player_)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    go_back = types.KeyboardButton('/start')
    markup.add(go_back)
    bot.send_sticker(chat, 'CAACAgIAAxkBAAL82mT6_I9XB991ig4amZAjx4_OgxwbAAKxGgAC3vWhS-cUzkOLVSQEMAQ')
    bot.send_message(chat, f'Штош... Возвращайся, если передумаешь...', reply_markup=markup)


def to_the_business(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kick = types.KeyboardButton('Удар!')
    hug = types.KeyboardButton('Обнимашки!')
    stat = types.KeyboardButton('Статистика.')
    stop = types.KeyboardButton('Я ухожу!')
    markup.add(kick, hug, stat, stop)
    bot.send_message(message.chat.id, 'Хочешь кого-нибудь ударить или обнять?', reply_markup=markup)


@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.reply_to(message, text)


def choose_func(message, action):
    user = message.from_user.username or message.from_user.first_name
    if action == 'Удар!':
        return kick_or_hug('kick', user)
    elif action == 'Обнимашки!':
        return kick_or_hug('hug', user)
    elif action == 'Статистика.':
        return statistic(user)
    elif action == 'Я ухожу!':
        i_am_out(message.chat.id, user)


@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text in ('Удар!', 'Обнимашки!', 'Статистика.'):
        bot.send_message(message.chat.id, choose_func(message, message.text))
    elif message.text == 'Я ухожу!':
        i_am_out(message.chat.id, message.from_user.username or message.from_user.first_name)
    #     answers_dict = {
    #         'Удар!': kick_or_hug('kick', message.from_user.username or message.from_user.first_name),
    #         'Обнимашки!': kick_or_hug('hug', message.from_user.username or message.from_user.first_name),
    #         'Статистика.': statistic(message.from_user.username or message.from_user.first_name),
    #         'Я ухожу!': i_am_out(message.chat.id, message.from_user.username or message.from_user.first_name),
    #
    #     }
    # # answer = answers_dict.get(message.text)
    # if message.text in answers_dict:
    #     return answers_dict[message.text]
    # # if answer:
    # #     bot.send_message(message.chat.id, answer)
    else:
        pass


bot.infinity_polling()
