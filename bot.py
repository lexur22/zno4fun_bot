# -*- coding: utf8 -*-
from dataclasses import dataclass
from pathlib import Path
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import LabeledPrice, ContentType
from aiogram import Bot, Dispatcher, executor, types
import os
import logging
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData
from dotenv import load_dotenv
import time
import json

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from aiogram.utils.markdown import link, hlink

connection = psycopg2.connect(user="ekluuomncseino",
                                  # пароль, который указали при установке PostgreSQL
                                  password="2ec04d6a5012351cb24622666dfa81f9494a5cd3267b837fec27c9e027df4598",
                                  host="ec2-54-75-184-144.eu-west-1.compute.amazonaws.com",
                                  port="5432",
                                  database="d5efhtlh8iiuqg")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
create_users_table = "CREATE TABLE IF NOT EXISTS information (id SERIAL PRIMARY KEY,user_id INTEGER NOT NULL, is_payment VARCHAR)"
cursor = connection.cursor()
cursor.execute(create_users_table)
connection.commit()



storage = MemoryStorage()   # обозначаем программе, где будут храниться наши состояния

# Подключение к базеданных
logging.basicConfig(level=logging.INFO)
env_path = Path('config.env')
load_dotenv(dotenv_path=env_path)

chat = os.getenv('CHAT_ID')
token = os.getenv('BOT_TOKEN')
providerToken = os.getenv('PROVIDER_TOKEN')

chat = str(chat)


bot = Bot(token=str(token))
dp = Dispatcher(bot, storage=storage)
vote_callback = CallbackData("vote", "action",)      # фабрика callback


# класс сосстояний, откуда собственно и будут браться состояния (все состояния мы задаем самостоятельно)
# если нам нужно задать состояние в одном из хедлеров, то нужно использовать метод .set() и имя состояния
# чтобы отследить любое состояние в хендлер необходимо передавать state='*' , где * - означает, что этот хендлер будет отслеживаться из любого состояния
# Задаем новый класс состояний
class Opportunities(StatesGroup):

    start = State()
    task = State()


# переходим к возможностям бота
@dp.message_handler(commands='start', state='*')      # обрабатываем кнопку 'start' и новое состояние
async def opportunities_bot(message: types.Message, state: FSMContext):

    info = await state.get_data()
    message_id = message.message_id
    user_id = message.from_user.id

    if len(str(user_id)) < 10:
        user_id = message.from_user.id
    else:
        user_id = info['user_id']

    print(user_id)

    await state.update_data(
        {
            'message_id': message_id
        }
    )

    # print(user_id)
    # print(message_id)


    # проверям, новый пользователь или нет
    cursor.execute(f'SELECT user_id FROM information WHERE user_id = {user_id}')
    check_user = cursor.fetchone()
    connection.commit()

    #проверяем статус оплаты
    cursor.execute(f'SELECT is_payment FROM information WHERE user_id = {user_id}')
    check_payment = cursor.fetchone()
    if check_payment != None:
        check_payment = check_payment[0]
        connection.commit()


    if (check_user == None) and (len(str(user_id)) < 10):
        entites = (str(user_id), 'unpaid',)
        request = f"INSERT INTO information (user_id, is_payment) VALUES {entites}"
        # print(request)
        connection.autocommit = True
        cursor.execute(request, entites)
        connection.commit()
        text = 'Вітаю! Я твій помічник при підготовці до ЗНО з фізики. Тут ти знайдеш усю необхідну інформацію для успішного складання екзамену'

        buttons = [
            types.InlineKeyboardButton(text="1", callback_data=vote_callback.new(action='task_1')),
            types.InlineKeyboardButton(text="2", callback_data=vote_callback.new(action='task_2')),
            types.InlineKeyboardButton(text="3", callback_data=vote_callback.new(action='task_3')),
            types.InlineKeyboardButton(text="4", callback_data=vote_callback.new(action='task_4')),
            types.InlineKeyboardButton(text="5", callback_data=vote_callback.new(action='task_5')),
            types.InlineKeyboardButton(text="6", callback_data=vote_callback.new(action='task_6')),
            types.InlineKeyboardButton(text="7", callback_data=vote_callback.new(action='task_7')),
            types.InlineKeyboardButton(text="8", callback_data=vote_callback.new(action='task_8')),
            types.InlineKeyboardButton(text="9", callback_data=vote_callback.new(action='task_9')),
            types.InlineKeyboardButton(text="10", callback_data=vote_callback.new(action='task_10')),
            types.InlineKeyboardButton(text="11", callback_data=vote_callback.new(action='task_11')),
            types.InlineKeyboardButton(text="12", callback_data=vote_callback.new(action='task_12')),
            types.InlineKeyboardButton(text="13", callback_data=vote_callback.new(action='task_13')),
            types.InlineKeyboardButton(text="14", callback_data=vote_callback.new(action='task_14')),
            types.InlineKeyboardButton(text="15", callback_data=vote_callback.new(action='task_15')),
            types.InlineKeyboardButton(text="16", callback_data=vote_callback.new(action='task_16')),
            types.InlineKeyboardButton(text="17", callback_data=vote_callback.new(action='task_17')),
            types.InlineKeyboardButton(text="18", callback_data=vote_callback.new(action='task_18')),
            types.InlineKeyboardButton(text="19", callback_data=vote_callback.new(action='task_19')),
            types.InlineKeyboardButton(text="20", callback_data=vote_callback.new(action='task_20')),
            types.InlineKeyboardButton(text="21", callback_data=vote_callback.new(action='task_21')),
            types.InlineKeyboardButton(text="22", callback_data=vote_callback.new(action='task_22')),
            types.InlineKeyboardButton(text="23", callback_data=vote_callback.new(action='task_23')),
            types.InlineKeyboardButton(text="24", callback_data=vote_callback.new(action='task_24')),
            types.InlineKeyboardButton(text="Отримати всі матеріали", callback_data=vote_callback.new(action='get_all'), pay=True),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
        keyboard.add(*buttons)
        buttons_admins = [
            types.InlineKeyboardButton(text="Детальна інформація", callback_data=vote_callback.new(action='get_all_information')),
        ]
        keyboard.row(*buttons_admins)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode='HTML')
        await Opportunities.task.set()
    elif check_payment == 'paid':
        text = 'Я твій помічник при підготовці до ЗНО з фізики. Тут ти знайдеш усю необхідну інформацію для успішного складання екзамену'

        buttons = [
            types.InlineKeyboardButton(text="1", callback_data=vote_callback.new(action='task_1')),
            types.InlineKeyboardButton(text="2", callback_data=vote_callback.new(action='task_2')),
            types.InlineKeyboardButton(text="3", callback_data=vote_callback.new(action='task_3')),
            types.InlineKeyboardButton(text="4", callback_data=vote_callback.new(action='task_4')),
            types.InlineKeyboardButton(text="5", callback_data=vote_callback.new(action='task_5')),
            types.InlineKeyboardButton(text="6", callback_data=vote_callback.new(action='task_6')),
            types.InlineKeyboardButton(text="7", callback_data=vote_callback.new(action='task_7')),
            types.InlineKeyboardButton(text="8", callback_data=vote_callback.new(action='task_8')),
            types.InlineKeyboardButton(text="9", callback_data=vote_callback.new(action='task_9')),
            types.InlineKeyboardButton(text="10", callback_data=vote_callback.new(action='task_10')),
            types.InlineKeyboardButton(text="11", callback_data=vote_callback.new(action='task_11')),
            types.InlineKeyboardButton(text="12", callback_data=vote_callback.new(action='task_12')),
            types.InlineKeyboardButton(text="13", callback_data=vote_callback.new(action='task_13')),
            types.InlineKeyboardButton(text="14", callback_data=vote_callback.new(action='task_14')),
            types.InlineKeyboardButton(text="15", callback_data=vote_callback.new(action='task_15')),
            types.InlineKeyboardButton(text="16", callback_data=vote_callback.new(action='task_16')),
            types.InlineKeyboardButton(text="17", callback_data=vote_callback.new(action='task_17')),
            types.InlineKeyboardButton(text="18", callback_data=vote_callback.new(action='task_18')),
            types.InlineKeyboardButton(text="19", callback_data=vote_callback.new(action='task_19')),
            types.InlineKeyboardButton(text="20", callback_data=vote_callback.new(action='task_20')),
            types.InlineKeyboardButton(text="21", callback_data=vote_callback.new(action='task_21')),
            types.InlineKeyboardButton(text="22", callback_data=vote_callback.new(action='task_22')),
            types.InlineKeyboardButton(text="23", callback_data=vote_callback.new(action='task_23')),
            types.InlineKeyboardButton(text="24", callback_data=vote_callback.new(action='task_24')),
            types.InlineKeyboardButton(text="Доступ до всіх матеріалів", callback_data=vote_callback.new(action='nothing'))
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
        keyboard.add(*buttons)
        buttons_admins = [
            types.InlineKeyboardButton(text="Детальна інформація", callback_data=vote_callback.new(action='get_all_information')),
        ]
        keyboard.row(*buttons_admins)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode='HTML')
        await Opportunities.task.set()
    else:
        text = 'Я твій помічник при підготовці до ЗНО з фізики. Тут ти знайдеш усю необхідну інформацію для успішного складання екзамену'

        buttons = [
            types.InlineKeyboardButton(text="1", callback_data=vote_callback.new(action='task_1')),
            types.InlineKeyboardButton(text="2", callback_data=vote_callback.new(action='task_2')),
            types.InlineKeyboardButton(text="3", callback_data=vote_callback.new(action='task_3')),
            types.InlineKeyboardButton(text="4", callback_data=vote_callback.new(action='task_4')),
            types.InlineKeyboardButton(text="5", callback_data=vote_callback.new(action='task_5')),
            types.InlineKeyboardButton(text="6", callback_data=vote_callback.new(action='task_6')),
            types.InlineKeyboardButton(text="7", callback_data=vote_callback.new(action='task_7')),
            types.InlineKeyboardButton(text="8", callback_data=vote_callback.new(action='task_8')),
            types.InlineKeyboardButton(text="9", callback_data=vote_callback.new(action='task_9')),
            types.InlineKeyboardButton(text="10", callback_data=vote_callback.new(action='task_10')),
            types.InlineKeyboardButton(text="11", callback_data=vote_callback.new(action='task_11')),
            types.InlineKeyboardButton(text="12", callback_data=vote_callback.new(action='task_12')),
            types.InlineKeyboardButton(text="13", callback_data=vote_callback.new(action='task_13')),
            types.InlineKeyboardButton(text="14", callback_data=vote_callback.new(action='task_14')),
            types.InlineKeyboardButton(text="15", callback_data=vote_callback.new(action='task_15')),
            types.InlineKeyboardButton(text="16", callback_data=vote_callback.new(action='task_16')),
            types.InlineKeyboardButton(text="17", callback_data=vote_callback.new(action='task_17')),
            types.InlineKeyboardButton(text="18", callback_data=vote_callback.new(action='task_18')),
            types.InlineKeyboardButton(text="19", callback_data=vote_callback.new(action='task_19')),
            types.InlineKeyboardButton(text="20", callback_data=vote_callback.new(action='task_20')),
            types.InlineKeyboardButton(text="21", callback_data=vote_callback.new(action='task_21')),
            types.InlineKeyboardButton(text="22", callback_data=vote_callback.new(action='task_22')),
            types.InlineKeyboardButton(text="23", callback_data=vote_callback.new(action='task_23')),
            types.InlineKeyboardButton(text="24", callback_data=vote_callback.new(action='task_24')),
            types.InlineKeyboardButton(text="Отримати всі матеріали", callback_data=vote_callback.new(action='get_all'),
                                       pay=True),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
        keyboard.add(*buttons)
        buttons_admins = [
            types.InlineKeyboardButton(text="Детальна інформація",
                                       callback_data=vote_callback.new(action='get_all_information')),
        ]
        keyboard.row(*buttons_admins)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode='HTML')
        await Opportunities.task.set()



# ПРОВЕРКА ПОДПИСКИ ДЛЯ ВСЕХ НОМЕРОВ, ЕСЛИ ПОЛЬЗОВАТЕЛЬ НЕ ОПЛАТИЛ СООБЩАЕМ ЕМУ ОБ ЭТОМ

# класс для созднания оплаты
@dataclass
class Item:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: list
    provider_data: dict = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    need_email: bool = False
    need_shipping_address: bool = False
    send_phone_number_to_provider: bool = False
    send_email_to_provider: bool = False
    is_flexible: bool = False
    provider_token: str = providerToken

    def generate_invoice(self):
        return self.__dict__


Course = Item(
    title='Повний матеріал до ЗНО з фізики',
    description='Купуючи цей курс, ви отримуєте структурований матеріал і повний розбір кожного завдання із ЗНО з фізики \n\n *Для оплати тестового платежу : \n  Номер картки - 4242 4242 4242 4242;\n  Дата - 12/34;\n  CVC - 444; \n  Будь-які значення для інших полів форми *\n\n',
    currency='UAH',
    prices=[
        LabeledPrice(
            label='Матеріал',
            amount=502_00
        )
    ],
    start_parameter='pay',
    is_flexible=False,
)


# обрабатываем кнопку оплаты
@dp.callback_query_handler(vote_callback.filter(action='get_all'), state='*')
async def get_all_theory(call: types.CallbackQuery, state: FSMContext):
    # тут что-то делается с оплатой
    user_id = call.from_user.id
    # stroke = f'UPDATE information SET is_payment = "paid" WHERE user_id={user_id}'  # обновляем информацию об оплате в таблице
    # cursor.execute(stroke)
    # connection.commit()
    # await call.message.edit_text('')
    # await call.answer()
    info = await state.get_data()
    await state.update_data(
        {
            'status': 'unpaid',
            'user_id': user_id,
        }
    )
    # print(info)
    keyboard = {
        "inline_keyboard":
        [
            [
                {
                    "text": 'Оплатити',
                    "pay": True
                }
            ],
            [
                {
                    "text": 'Меню',
                    "callback_data": vote_callback.new(action='menu_fromPay')
                }
            ],
        ]
    }
    keyboard = json.dumps(keyboard)
    message_id = call.message.message_id
    await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)
    await bot.send_invoice(call.message.chat.id, **Course.generate_invoice(), payload='paid', reply_markup=keyboard)
    await call.answer(cache_time=1)
    await state.reset_state(with_data=False)


# обрабатываем состояние оплаты
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True, error_message='Ошибка')


# проверяем статус платежа
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state='*')
async def check_payment(status: types.SuccessfulPayment, state: FSMContext):
    status = status['successful_payment']['invoice_payload']
    info = await state.get_data()
    user_id = info['user_id']
    request = f"UPDATE information SET is_payment = 'paid' WHERE user_id={user_id}"
    connection.autocommit = True
    cursor.execute(request)
    connection.commit()
    if status == 'paid':
        # добавить обновление статуса оплаты сюда
        await state.update_data(
            {
                'status': status,
            }
        )
    else:
        await state.update_data(
            {
                'status': 'unpaid',
            }
        )


# обрабатываем кнопку меню, из оплаты
@dp.callback_query_handler(vote_callback.filter(action='menu_fromPay'), state='*')
async def answer_for_back_menu(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    status = info['status']
    # print(status)
    if status == 'paid':

        user_id = info['user_id']
        request = f"UPDATE information SET is_payment = 'paid' WHERE user_id={user_id}"
        connection.autocommit = True
        cursor.execute(request)
        connection.commit()


        message_id = call.message.message_id
        await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)

        await state.update_data(
            {
                'message_id': (message_id + 1),
            }
        )

        text = 'Я твій помічник при підготовці до ЗНО з фізики Тут ти знайдеш усю необхідну інформацію для успішного складання екзамену. \n\n Якщо виникли якісь проблеми - @mishkekich'

        buttons = [
            types.InlineKeyboardButton(text="1", callback_data=vote_callback.new(action='task_1')),
            types.InlineKeyboardButton(text="2", callback_data=vote_callback.new(action='task_2')),
            types.InlineKeyboardButton(text="3", callback_data=vote_callback.new(action='task_3')),
            types.InlineKeyboardButton(text="4", callback_data=vote_callback.new(action='task_4')),
            types.InlineKeyboardButton(text="5", callback_data=vote_callback.new(action='task_5')),
            types.InlineKeyboardButton(text="6", callback_data=vote_callback.new(action='task_6')),
            types.InlineKeyboardButton(text="7", callback_data=vote_callback.new(action='task_7')),
            types.InlineKeyboardButton(text="8", callback_data=vote_callback.new(action='task_8')),
            types.InlineKeyboardButton(text="9", callback_data=vote_callback.new(action='task_9')),
            types.InlineKeyboardButton(text="10", callback_data=vote_callback.new(action='task_10')),
            types.InlineKeyboardButton(text="11", callback_data=vote_callback.new(action='task_11')),
            types.InlineKeyboardButton(text="12", callback_data=vote_callback.new(action='task_12')),
            types.InlineKeyboardButton(text="13", callback_data=vote_callback.new(action='task_13')),
            types.InlineKeyboardButton(text="14", callback_data=vote_callback.new(action='task_14')),
            types.InlineKeyboardButton(text="15", callback_data=vote_callback.new(action='task_15')),
            types.InlineKeyboardButton(text="16", callback_data=vote_callback.new(action='task_16')),
            types.InlineKeyboardButton(text="17", callback_data=vote_callback.new(action='task_17')),
            types.InlineKeyboardButton(text="18", callback_data=vote_callback.new(action='task_18')),
            types.InlineKeyboardButton(text="19", callback_data=vote_callback.new(action='task_19')),
            types.InlineKeyboardButton(text="20", callback_data=vote_callback.new(action='task_20')),
            types.InlineKeyboardButton(text="21", callback_data=vote_callback.new(action='task_21')),
            types.InlineKeyboardButton(text="22", callback_data=vote_callback.new(action='task_22')),
            types.InlineKeyboardButton(text="23", callback_data=vote_callback.new(action='task_23')),
            types.InlineKeyboardButton(text="24", callback_data=vote_callback.new(action='task_24')),
            types.InlineKeyboardButton(text="Доступ до всіх матеріалів", callback_data=vote_callback.new(action='nothing'))
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
        keyboard.add(*buttons)
        buttons_admins = [
            types.InlineKeyboardButton(text="Детальна інформація",
                                       callback_data=vote_callback.new(action='get_all_information')),
        ]
        keyboard.row(*buttons_admins)
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)
        await Opportunities.task.set()
    else:
        message_id = call.message.message_id
        await bot.delete_message(chat_id=call.message.chat.id, message_id=message_id)

        await state.update_data(
            {
                'message_id': (message_id + 1),
            }
        )

        text = 'Я твій помічник при підготовці до ЗНО з фізики. Тут ти знайдеш усю необхідну інформацію для успішного складання екзамену. \n\n Якщо виникли якісь проблеми - @mishkekich'

        buttons = [
            types.InlineKeyboardButton(text="1", callback_data=vote_callback.new(action='task_1')),
            types.InlineKeyboardButton(text="2", callback_data=vote_callback.new(action='task_2')),
            types.InlineKeyboardButton(text="3", callback_data=vote_callback.new(action='task_3')),
            types.InlineKeyboardButton(text="4", callback_data=vote_callback.new(action='task_4')),
            types.InlineKeyboardButton(text="5", callback_data=vote_callback.new(action='task_5')),
            types.InlineKeyboardButton(text="6", callback_data=vote_callback.new(action='task_6')),
            types.InlineKeyboardButton(text="7", callback_data=vote_callback.new(action='task_7')),
            types.InlineKeyboardButton(text="8", callback_data=vote_callback.new(action='task_8')),
            types.InlineKeyboardButton(text="9", callback_data=vote_callback.new(action='task_9')),
            types.InlineKeyboardButton(text="10", callback_data=vote_callback.new(action='task_10')),
            types.InlineKeyboardButton(text="11", callback_data=vote_callback.new(action='task_11')),
            types.InlineKeyboardButton(text="12", callback_data=vote_callback.new(action='task_12')),
            types.InlineKeyboardButton(text="13", callback_data=vote_callback.new(action='task_13')),
            types.InlineKeyboardButton(text="14", callback_data=vote_callback.new(action='task_14')),
            types.InlineKeyboardButton(text="15", callback_data=vote_callback.new(action='task_15')),
            types.InlineKeyboardButton(text="16", callback_data=vote_callback.new(action='task_16')),
            types.InlineKeyboardButton(text="17", callback_data=vote_callback.new(action='task_17')),
            types.InlineKeyboardButton(text="18", callback_data=vote_callback.new(action='task_18')),
            types.InlineKeyboardButton(text="19", callback_data=vote_callback.new(action='task_19')),
            types.InlineKeyboardButton(text="20", callback_data=vote_callback.new(action='task_20')),
            types.InlineKeyboardButton(text="21", callback_data=vote_callback.new(action='task_21')),
            types.InlineKeyboardButton(text="22", callback_data=vote_callback.new(action='task_22')),
            types.InlineKeyboardButton(text="23", callback_data=vote_callback.new(action='task_23')),
            types.InlineKeyboardButton(text="24", callback_data=vote_callback.new(action='task_24')),
            types.InlineKeyboardButton(text="Отримати всі матеріали", callback_data=vote_callback.new(action='get_all'),
                                       pay=True),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
        keyboard.add(*buttons)
        buttons_admins = [
            types.InlineKeyboardButton(text="Детальна інформація",
                                       callback_data=vote_callback.new(action='get_all_information')),
        ]
        keyboard.row(*buttons_admins)
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)
        await Opportunities.task.set()


# получаем полную информацию о теории
@dp.callback_query_handler(vote_callback.filter(action='get_all_information'), state='*')
async def get_all_information_about_theory(call: types.CallbackQuery, state: FSMContext):
    buttons = [
        types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*buttons)
    text = 'Я твій помічник при підготовці до ЗНО з фізики. Тут ти знайдеш усю необхідну інформацію для успішного складання.'
    text = text + 'Ви отримуєте структурований матеріал і повний розбір кожного завдання із ЗНО з фізики. Для пояснення завдання ми наводимо різні рішення, а також наочно показуємо, які рішення краще і чому.'
    await call.message.edit_text(text=text, parse_mode='HTML', reply_markup=keyboard)
    await call.answer(cache_time=1)


# сообщаем о пустышке (если она есть)
@dp.callback_query_handler(vote_callback.filter(action='nothing'), state='*')
async def answer_about_pass(call: types.CallbackQuery, state: FSMContext):
    text = 'Це пуста кнопка, натисніть на іншу'
    await call.answer(text=text, cache_time=1)


# обрабатываем кнопку меню
@dp.callback_query_handler(vote_callback.filter(action='menu'), state='*')
async def back_for_menu(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.update_data(
        {
            'user_id': call.from_user.id,
        }
    )
    await opportunities_bot(call.message, state)
    await call.answer()


# обрабатываем кнопку вперед
@dp.callback_query_handler(vote_callback.filter(action='prev'), state=Opportunities.task)
async def show_next_task(call: types.CallbackQuery, callback_data: vote_callback, state: FSMContext):
    info = await state.get_data()
    user_id = call.from_user.id
    await state.update_data(
        {
            'user_id': user_id
        }
    )
    stroke = f"SELECT is_payment FROM information WHERE user_id = " + str(user_id)
    cursor.execute(stroke)
    state_payment = cursor.fetchone()[0]
    connection.commit()

    number_of_task = info['number_of_task']


    if state_payment == 'unpaid':
        if number_of_task == 1:
            await answer_for_free_documentation_task_2(call, state)
        elif number_of_task == 2:
            await answer_for_free_documentation_task_3(call, state)
        elif number_of_task == 3:
            text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
            await call.answer(text=text, show_alert=True)
    else:
        if number_of_task == 1:
            await answer_for_free_documentation_task_2(call, state)
        elif number_of_task == 2:
            await answer_for_free_documentation_task_3(call, state)
        if number_of_task == 3:
            await answer_for_unpaid_task_4(call, state)
        elif number_of_task == 4:
            await answer_for_unpaid_task_5(call, state)
        elif number_of_task == 5:
            await answer_for_unpaid_task_6(call, state)
        elif number_of_task == 6:
            await answer_for_unpaid_task_7(call, state)
        elif number_of_task == 7:
            await answer_for_unpaid_task_8(call, state)
        elif number_of_task == 8:
            await answer_for_unpaid_task_9(call, state)
        elif number_of_task == 9:
            await answer_for_unpaid_task_10(call, state)
        elif number_of_task == 10:
            await answer_for_unpaid_task_11(call, state)
        elif number_of_task == 11:
            await answer_for_unpaid_task_12(call, state)
        elif number_of_task == 12:
            await answer_for_unpaid_task_13(call, state)
        elif number_of_task == 13:
            await answer_for_unpaid_task_14(call, state)
        elif number_of_task == 14:
            await answer_for_unpaid_task_15(call, state)
        elif number_of_task == 15:
            await answer_for_unpaid_task_16(call, state)
        elif number_of_task == 16:
            await answer_for_unpaid_task_17(call, state)
        elif number_of_task == 17:
            await answer_for_unpaid_task_18(call, state)
        elif number_of_task == 18:
            await answer_for_unpaid_task_19(call, state)
        elif number_of_task == 19:
            await answer_for_unpaid_task_20(call, state)
        elif number_of_task == 20:
            await answer_for_unpaid_task_21(call, state)
        elif number_of_task == 21:
            await answer_for_unpaid_task_22(call, state)
        elif number_of_task == 22:
            await answer_for_unpaid_task_23(call, state)
        elif number_of_task == 23:    
            await answer_for_unpaid_task_24(call, state)
        elif number_of_task == 24:
            await answer_for_free_documentation_task_1(call, state)


# обрабатываем кнопку назад
@dp.callback_query_handler(vote_callback.filter(action='back'), state=Opportunities.task)
async def show_next_task(call: types.CallbackQuery, callback_data: vote_callback, state: FSMContext):
    info = await state.get_data()
    user_id = call.from_user.id
    await state.update_data(
        {
            'user_id': user_id
        }
    )
    stroke = f"SELECT is_payment FROM information WHERE user_id = " + str(user_id)
    cursor.execute(stroke)
    state_payment = cursor.fetchone()[0]
    connection.commit()

    number_of_task = info['number_of_task']


    if state_payment == 'unpaid':
        if number_of_task == 3:
            await answer_for_free_documentation_task_2(call, state)
        elif number_of_task == 2:
            await answer_for_free_documentation_task_1(call, state)
        elif number_of_task == 1:
            text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
            await call.answer(text=text, show_alert=True)
    else:
        if number_of_task == 1:
            await answer_for_unpaid_task_24(call, state)
        elif number_of_task == 24:
            await answer_for_unpaid_task_23(call, state)
        elif number_of_task == 23:
            await answer_for_unpaid_task_22(call, state)
        if number_of_task == 22:
            await answer_for_unpaid_task_21(call, state)
        elif number_of_task == 21:
            await answer_for_unpaid_task_20(call, state)
        elif number_of_task == 20:
            await answer_for_unpaid_task_19(call, state)
        elif number_of_task == 19:
            await answer_for_unpaid_task_18(call, state)
        elif number_of_task == 18:
            await answer_for_unpaid_task_17(call, state)
        elif number_of_task == 17:
            await answer_for_unpaid_task_16(call, state)
        elif number_of_task == 16:
            await answer_for_unpaid_task_15(call, state)
        elif number_of_task == 15:
            await answer_for_unpaid_task_14(call, state)
        elif number_of_task == 14:
            await answer_for_unpaid_task_13(call, state)
        elif number_of_task == 13:
            await answer_for_unpaid_task_12(call, state)
        elif number_of_task == 12:
            await answer_for_unpaid_task_11(call, state)
        elif number_of_task == 11:
            await answer_for_unpaid_task_10(call, state)
        elif number_of_task == 10:
            await answer_for_unpaid_task_9(call, state)
        elif number_of_task == 9:
            await answer_for_unpaid_task_8(call, state)
        elif number_of_task == 8:
            await answer_for_unpaid_task_7(call, state)
        elif number_of_task == 7:
            await answer_for_unpaid_task_6(call, state)
        elif number_of_task == 6:
            await answer_for_unpaid_task_5(call, state)
        elif number_of_task == 5:
            await answer_for_unpaid_task_4(call, state)
        elif number_of_task == 4:
            await answer_for_free_documentation_task_3(call, state)
        elif number_of_task == 3:
            await answer_for_free_documentation_task_2(call, state)
        elif number_of_task == 2:
            await answer_for_free_documentation_task_1(call, state)


# номер 1
@dp.callback_query_handler(vote_callback.filter(action='task_1'), state=Opportunities.task)
async def answer_for_free_documentation_task_1(call: types.CallbackQuery, state: FSMContext):
 
        info = await state.get_data()
        message_id = info['message_id']
        text = '<b>Завдання №1</b>\n\n'
        text = text + "Перш ніж приступити до виконання цього завдання слід звернути увагу на теми «Механіка» та «Основи кінематики» \n"
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1yjjYFBYlFNFCbDj_VKMPPmh0jmzWTRP0/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання ', url='https://drive.google.com/file/d/1wgo80FoSPPzTTvymmCyxWkyBlqezndhA/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        #keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await state.update_data({
            'number_of_task': 1,
        })

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)


# номер 2
@dp.callback_query_handler(vote_callback.filter(action='task_2'), state=Opportunities.task)
async def answer_for_free_documentation_task_2(call: types.CallbackQuery, state: FSMContext):
    
        info = await state.get_data()
        message_id = info['message_id']

        text = '<b>Завдання №2</b>\n\n'
        text = text + 'Для виконання цього завдання слід звернути увагу на теми «Механіка» та «Основи динаміки»\n'

        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1Ijd5uEWR8lMRDs8nee8xB_eqhrm23fOU/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1jTI9WNi7x9uLKb883T0Y-pu4thNUt_w6/view?usp=sharing'),
            types.InlineKeyboardButton(text='Третій тип завдання', url='https://drive.google.com/file/d/14L53Vj2n1LIiYFvOCferP3y1KBmS8ZW6/view?usp=sharing'),

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        #keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await state.update_data({
            'number_of_task': 2,
        })

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)


# номер 3
@dp.callback_query_handler(vote_callback.filter(action='task_3'), state=Opportunities.task)
async def answer_for_free_documentation_task_3(call: types.CallbackQuery, state: FSMContext):

        info = await state.get_data()
        message_id = info['message_id']

        text = '<b>Завдання №3</b>\n\n'
        text = text + 'Дане завдання включає в себе поняття із розділу механіки, про закон збереження в механіці і рівномірний рух по колу\n'

        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1gRJ6LN8REfe8s-l7SwMYBclJRhnXL4HL/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1S4ebj8KhRlahyKA6FP_HcRcRtKYhbgCA/view?usp=sharing'),
            types.InlineKeyboardButton(text='Третій тип завдання', url='https://drive.google.com/file/d/1wGZm0PR3weD_f0fvbxLNnkqPH0iDt8RA/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        #keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await state.update_data({
            'number_of_task': 3,
        })

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)


# номер 4
@dp.callback_query_handler(vote_callback.filter(action='task_4'), state=Opportunities.task)
async def answer_for_unpaid_task_4(call: types.CallbackQuery, state: FSMContext):

    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]


    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №4</b>\n\n'
        text = text + 'Завдання вимагає розуміння властивостей елементів елементів рідин і газів\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1ZAHn0hoYNKKoJS5_5YENrIpBEg8KwA2b/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1S0YMdD0lI7Hz5MN1LnM-O_qZQtTSIDYd/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 4,
    })


# номер 5
@dp.callback_query_handler(vote_callback.filter(action='task_5'), state=Opportunities.task)
async def answer_for_unpaid_task_5(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №5</b>\n\n'
        text = text + 'Завдання скеровано на перевірку розуміння властивостей газів, рідин і твердих тіл\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1qXjhk7TJnJAd2cPah48nO5ER5AR3e3lF/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1-ArHVAyJioshYocQVq0zFj0KA3g550Z2/view?usp=sharing'),

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 5,
    })


# номер 6
@dp.callback_query_handler(vote_callback.filter(action='task_6'), state=Opportunities.task)
async def answer_for_unpaid_task_6(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №6</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання розуміння поняття ізопроцесів, внутрішньої енергії і вміння розрахувати роботу в термодинамічних процесах\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1VPvtL6xgHbSAaR7cFUzD-HpQLZUyQWPh/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1ddpBGNL_IUHtv7rGPMxfY1h-sQqdnVZ-/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 6,
    })


# номер 7
@dp.callback_query_handler(vote_callback.filter(action='task_7'), state=Opportunities.task)
async def answer_for_unpaid_task_7(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №7</b>\n\n'
        text = text + 'Для виконання цього завдання слід на теми молекулярної фізики й термодинаміки\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1pET6OrDdyvpPQt6FiMytOUTDt9RdhaFk/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1Cfgb9yODLJvZvgzbpzOPj-p7RWzVJRkl/view?usp=sharing'),

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 7,
    })


# номер 8
@dp.callback_query_handler(vote_callback.filter(action='task_8'), state=Opportunities.task)
async def answer_for_unpaid_task_8(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №8</b>\n\n'
        text = text + 'Дане завдання має відношення до розділу елекродинаміки, а саме основ електростатики та явищ й законів електромагнітної індукції\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1LhcxdNiwKOVJkJc5hu6jZJeHc45-GVH7/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/13u5kmXStqWjJ-x6Qp6orXmSacLaksoce/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 8,
    })


# номер 9
@dp.callback_query_handler(vote_callback.filter(action='task_9'), state=Opportunities.task)
async def answer_for_unpaid_task_9(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №9</b>\n\n'
        text = text + 'Для виконання цього завдання слід розуміти в розділі електродинаміки, зокрема закони постійного струму, магнітне поле і явище магнітної індукції\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1XYpV4JjTOoZX-DnjdLob5Dt2zGQ1Ge_q/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1YfYnFAEP1pYEunGD-z0NN9chlv39l1pm/view?usp=sharing'),
            types.InlineKeyboardButton(text='Третій тип завдання', url='https://drive.google.com/file/d/1_JXhQsNWfEM9XwDOUD1GQpVfmDQR5iuf/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 9,
    })


# номер 10
@dp.callback_query_handler(vote_callback.filter(action='task_10'), state=Opportunities.task)
async def answer_for_unpaid_task_10(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №10</b>\n\n'
        text = text + 'Для успішного рішення цього завдання слід розумітися в темах електромагнітних коливань, магнітного поля та явища магнітної індукції\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1D5qYV3tfVp2G9INYiwjJlvY_1d8GP00f/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/18i6FpIv3W6HtjGUbCGp6R9jdrRncx-au/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 10,
    })


# номер 11
@dp.callback_query_handler(vote_callback.filter(action='task_11'), state=Opportunities.task)
async def answer_for_unpaid_task_11(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №11</b>\n\n'
        text = text + 'Основою завдання є розділ оптики, зокрема закон заломлення світла\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1t-7K8b4VQORHQWPnfznbMRyB60I4ytkn/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/17tHtUF7fd90tN-ITMrIl6wqgezBBR16i/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 11,
    })


# номер 12
@dp.callback_query_handler(vote_callback.filter(action='task_12'), state=Opportunities.task)
async def answer_for_unpaid_task_12(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №12</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання розуміння корпусклярно-ївильвої природи світла і явищ інтерференції, дифрації, дисперсії і фотоефекту\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1uqv3_sz0S4pSAl29Qfsjnlbb4O_PswSW/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1QRxxXNWJYCkZd7jWaLG7B3U20-EYVHQ-/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 12,
    })


# номер 13
@dp.callback_query_handler(vote_callback.filter(action='task_13'), state=Opportunities.task)
async def answer_for_unpaid_task_13(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №13</b>\n\n'
        text = text + 'Для виконання цього завдання слід звернути увагу на теми «Квантова фізика» та «Атом й атомне ядро»\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1Vbh5T4vGwqW-m5RoCKHqrk7ZOXGkFn7P/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/173eG9PaGRNCAtdepr49N_Pi-42BvHwQf/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 13,
    })


# номер 14
@dp.callback_query_handler(vote_callback.filter(action='task_14'), state=Opportunities.task)
async def answer_for_unpaid_task_14(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №14</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання розуміння процесу ядерного розпаду й вміння аланізувати рівняння ядерних реакцій\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1upDUFqot1JL_QJDPEo57ULAHiohCIbOK/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1ZloNARc_8dEmeK_EW1zKkiqnJRDNhSaE/view?usp=sharing'),

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 14,
    })


# номер 15
@dp.callback_query_handler(vote_callback.filter(action='task_15'), state=Opportunities.task)
async def answer_for_unpaid_task_15(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №15</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання вміння вирішувати розрахункові задачі із додавання швидкостей\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Завдання', url='https://drive.google.com/file/d/1PTY94yvZwvTOQ9eMx2PSu5-WY9CtFN3r/view?usp=sharing'),

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 15,
    })


# номер 16
@dp.callback_query_handler(vote_callback.filter(action='task_16'), state=Opportunities.task)
async def answer_for_unpaid_task_16(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №16</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання вміння вирішувати розрахукові задачі про механічні хвилі і коливання, а також вміння вміння використовувати закон збереження імпульс на практиці\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1Snp8F2QSpwFUKYxMdv0gMgJwa83tggQG/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1yEgmFaWEO-u0spAt09npNITjn1ffzBy5/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 16,
    })


# номер 17
@dp.callback_query_handler(vote_callback.filter(action='task_17'), state=Opportunities.task)
async def answer_for_unpaid_task_17(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №17</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання вміння аналізувати графіки ізопроцесів та рівняння стану ідеального газу\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1OgdntVHocZsyHmJW5Wqb1b0_jLmeYdXx/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/11_WwSO1Xe7Z-aGpdHqinJfPr0lHHxnM8/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 17,
    })


# номер 18
@dp.callback_query_handler(vote_callback.filter(action='task_18'), state=Opportunities.task)
async def answer_for_unpaid_task_18(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №18</b>\n\n'
        text = text + 'Завдання скеровано на перевірку вміння розв’язувати розрахункові задачі за допомогою закону Ома для повного кола, а також вміння інтерпретувати схеми електричного кола\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1VM3kwd69fPw2l7DpKUsB1_fuRxDoiv8M/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1MOPApNkfkZVCh_c-KLAr1p4majpQCMGa/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 18,
    })


# номер 19
@dp.callback_query_handler(vote_callback.filter(action='task_19'), state=Opportunities.task)
async def answer_for_unpaid_task_19(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №19</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання вміння вирішувати розрахункові задачі із розділів механіки і основ динаміки\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1MuADQ8TojUWnHji4L6JS84KvSCw62j9c/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1nGV4TAtztumN0frH5Pd1vvvo56OozwGe/view?usp=sharing'),
            types.InlineKeyboardButton(text='Третій тип завдання', url='https://drive.google.com/file/d/1lXpii9ozLWh6OIwqMt1rOXlc59cBo6dq/view?usp=sharing'),
            types.InlineKeyboardButton(text='Четвертий тип завдання', url='https://drive.google.com/file/d/1_9HcsHYp0JtmbBXa8txGdt8zKpXyJo97/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 19,
    })


# номер 20
@dp.callback_query_handler(vote_callback.filter(action='task_20'), state=Opportunities.task)
async def answer_for_unpaid_task_20(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №20</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання вміння вирішувати розрахункові задачі із розділів молекулярної фізики і термодинаміки\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1tAS8oLX0h8Jp5VKaRePvjFxVGapwOxgO/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1hIo-Uqnnw1gZvqf4jkYqi9Qhxcxtd99V/view?usp=sharing'),
            types.InlineKeyboardButton(text='Третій тип завдання', url='https://drive.google.com/file/d/1hIo-Uqnnw1gZvqf4jkYqi9Qhxcxtd99V/view?usp=sharing'),
            types.InlineKeyboardButton(text='Четвертий тип завдання', url='https://drive.google.com/file/d/1Aaq_-rjQTTUlKOmE1R-GW_UvqwvNMefa/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 20,
    })


# номер 21
@dp.callback_query_handler(vote_callback.filter(action='task_21'), state=Opportunities.task)
async def answer_for_unpaid_task_21(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №21</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання вміння вирішувати розрахункові задачі із розділу електродинаміки\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1FrLI3-m4qnmSk99VHg3EaPgnXnpup5V9/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1VXFTQrUCoEewSD76E2Q2eN4VEYbJ1MIB/view?usp=sharing'),
            types.InlineKeyboardButton(text='Третій тип завдання', url='https://drive.google.com/file/d/1AN1iQVIyjMFpzPS0qPv73j4qORsZ6UvM/view?usp=sharing'),
            types.InlineKeyboardButton(text='Четвертий тип завдання ', url='https://drive.google.com/file/d/1wvY7mtB3DrmNNWGMhoBKKhaNtr5c94Af/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 21,
    })


# номер 22
@dp.callback_query_handler(vote_callback.filter(action='task_22'), state=Opportunities.task)
async def answer_for_unpaid_task_22(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №22</b>\n\n'
        text = text + 'Завдання скеровано на оцінювання вміння розв’язувати розрахункові задачі пов’язаними із механічними коливаннями\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1QoEDh5tDQaAUQwWXj36g7MOOOjj0WgsG/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1kX0mUCn9_bR--ZkCCvp3KvgqRM8dnlpG/view?usp=sharing'),

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 22,
    })


# номер 23
@dp.callback_query_handler(vote_callback.filter(action='task_23'), state=Opportunities.task)
async def answer_for_unpaid_task_23(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №23</b>\n\n'
        text = text + 'Завдання скеровано на перевірку вміння розв’язувати розрахункові задачі із розділу оптики\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1o9NZf2GR_JgWjYBBu_dM7Et4eILiAkwJ/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1YerpNHSGGGhYhyDc2N3bZxpYs2npIdUt/view?usp=sharing'),

        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 23,
    })

    
# номер 24
@dp.callback_query_handler(vote_callback.filter(action='task_24'), state=Opportunities.task)
async def answer_for_unpaid_task_24(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    stroke = f'SELECT is_payment FROM information WHERE user_id = ' + str(info['user_id'])
    cursor.execute(stroke)
    connection.commit()
    state_payment = cursor.fetchone()
    state_payment = state_payment[0]

    if state_payment == 'unpaid':
        text = 'Вам недоступний цей номер, оскільки ви не оплатили матеріал'
        await call.answer(text=text, show_alert=True, cache_time=1)
    else:
        text = '<b>Завдання №24</b>\n\n'
        text = text + 'Завдання скеровано на перевірку вміння розв’язувати комплексні задачі із розділу квантової фізики\n'
        
        # кнопки с сылками на pdf файлы
        buttons = [
            types.InlineKeyboardButton(text='Перший тип завдання', url='https://drive.google.com/file/d/1kQGTjspJseqhJUwY6r04lmOLcBSrZxto/view?usp=sharing'),
            types.InlineKeyboardButton(text='Другий тип завдання', url='https://drive.google.com/file/d/1nQU5hmsr6RdfZdUvMpO8GfDpnHX7aELP/view?usp=sharing'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)
        # служебные кнопки
        buttons_admins = [
            types.InlineKeyboardButton(text="Назад", callback_data=vote_callback.new(action='back')),
            types.InlineKeyboardButton(text="Меню", callback_data=vote_callback.new(action='menu')),
            types.InlineKeyboardButton(text="Вперед", callback_data=vote_callback.new(action='prev')),
        ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=False)
        keyboard.row(*buttons_admins)

        await call.message.edit_text(text=text, reply_markup=keyboard, parse_mode='HTML')
        await call.answer(cache_time=1)

    await state.update_data({
        'number_of_task': 24,
    })

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)   # функция on_startup запускает именно ту функцию, которую нужно отправить куда-либо
