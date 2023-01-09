from bot_config import dp, bot
from aiogram import types
from random import randint
from pytube import YouTube
from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

total = 150
turn = 1

@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_message(message.from_user.id, text=f'Игра "Конфетки" На столе 150 конфет')
    await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}, '
                                                      f'начинаем игру?')
    button_yes = KeyboardButton('Да')
    button_no = KeyboardButton('Нет')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_yes, button_no)
    await message.reply('Ты любишь сладкое?', reply_markup=greet_kb)

@dp.message_handler(text=['Загрузить'])
async def yt_downloader(message: types.Message):
    await bot.send_message(message.from_user.id, text=f'Хорошо! {message.from_user.first_name}, '
                                                      f'Видеоролик будет загружен на твой компьютер!')
    file_name = 'https://www.youtube.com/watch?v=0P9odR9_FQ4'
    yt_video = YouTube(file_name)
    yt_video.streams.filter(resolution='360p', file_extension='mp4').first().download()



@dp.message_handler(text=['Да', 'Нет'])
async def start_play(message: types.Message):
    global total
    global turn
    total = 150
    if message.text:
        await bot.send_message(message.from_user.id, text=f'Хорошо! {message.from_user.first_name}, '
                                                          f'определим, кто ходит первым')
        turn = randint(0, 1)
        if turn == 1:
            await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}, первый ход у тебя')
            await bot.send_message(message.from_user.id,
                                   text=f'{message.from_user.first_name}, напиши сколько возьмешь конфет')
        else:
            await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name},'
                                                              f' первый ход у бота')
            sweets = randint(1, 28)
            total -= int(sweets)
            await bot.send_message(message.from_user.id, f'Бот взял {sweets} и теперь на столе осталось: {total}')
            await bot.send_message(message.from_user.id,
                                   text=f'{message.from_user.first_name}. Сколько ты хочешь взять?')
            turn = 1

@dp.message_handler()
async def anything(message: types.Message):
    global total
    global turn
    if turn == 1 and total > 28:
        if message.text.isdigit() and 0 < int(message.text) < 29:
            total -= int(message.text)
            await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, ты взял {message.text}. '
                                                         f'На столе осталось {total}')
            turn = 0
        if message.text.isdigit() and int(message.text) >= 29:
            await message.reply(f'{message.from_user.first_name} да ты жадина! Можно взять от 1 до 28 штук')
            await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}. '
                                                              f'Сколько ты хочешь опять взять?')
    if turn == 0 and total > 28:
        sweets = randint(1, 29)
        total -= int(sweets)
        await bot.send_message(message.from_user.id, f'Бот взял {sweets} и на столе осталось: {total}')
        if total > 28:
            await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name}. '
                                                              f'Сколько ты хочешь опять взять?')
        turn = 1
    if message.text.isdigit() and turn == 1 and total <= 28:
        await bot.send_message(message.from_user.id,
                               f'{message.from_user.first_name}, ты взял последние {total}'
                               f' Ты победил!')
        button_want = KeyboardButton('Загрузить')
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_want)
        await message.reply('Ты победил! Нажми кнопку для загрузки видеоролика', reply_markup=greet_kb)
    if turn == 0 and total <= 28:
        await bot.send_message(message.from_user.id,
                               f'Бот взял последние {total}'
                               f'и победил!')


