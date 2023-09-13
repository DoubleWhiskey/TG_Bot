import telebot
from config import TOKEN
from telebot import types

from speech_recognition_logic import recognize_speech, download_file
from fight_or_hug_logic import kick_or_hug
from orm_database import *

bot = telebot.TeleBot(TOKEN)


def database_check(message):
    if isinstance(message, str):
        return message in all_players()
    else:
        user = message.from_user.username or message.from_user.first_name
        return user in all_players()


def join_the_club(message, user):
    add_player(user)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    club = types.KeyboardButton('Я в деле!')
    pussy = types.KeyboardButton('Я пуська(')
    markup.add(club, pussy)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAL81mT6_C5Phnx_6qbrm8h3ctGRHtnHAAL9GgACNeKgS3dqE61odyNCMAQ')
    bot.send_message(message.chat.id, f"Привет, {user}! Хочешь вступить в наш клуб?", reply_markup=markup)


@bot.message_handler(commands=['start'])
def say_hi(message):
    user = message.from_user.username or message.from_user.first_name
    if database_check(message):
        to_the_business(message)
    else:
        join_the_club(message, user)


def i_am_in(message):
    if database_check(message):
        chat = message.chat.id
        bot.send_sticker(chat, 'CAACAgIAAxkBAAL82GT6_E3SRxAY6bqYCoVA3Xs9Al3mAAKmGQACaWehS61jIKeOdobtMAQ')
        bot.send_message(chat, f'Добро пожаловать в клуб!\nНе забывай правила...')
        to_the_business(message)
    else:
        say_hi(message)


def i_am_out(chat, _player_):
    if database_check(_player_):
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
    elif action == 'Список':
        result = ', '.join(all_players())
        return result or 'Никого нет'


@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text in ('Удар!', 'Обнимашки!', 'Статистика.', 'Список'):
        if not database_check(message):
            return say_hi(message)
        else:
            bot.send_message(message.chat.id, choose_func(message, message.text))
    elif message.text in ('Я ухожу!', 'Я пуська('):
        if not database_check(message):
            return say_hi(message)
        else:
            i_am_out(message.chat.id, message.from_user.username or message.from_user.first_name)
    elif message.text == 'Я в деле!':
        if not database_check(message):
            return say_hi(message)
        else:
            i_am_in(message)
    else:
        pass


bot.infinity_polling()
