import random
from datetime import datetime

from aiogram import types, Router, Bot
from aiogram.client.session import aiohttp
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import xml.etree.ElementTree as ET

from random import randint

from bot.utils.config_reader import config

rss_url = 'https://news.radio-t.com/rss'
rss_url1 = 'https://pp-prozozh.ru/recepty/feed'
bot = Bot(token=config.token)


class InputTime(StatesGroup):
  choosing_seconds = State()
  choosing_minutes = State()
  choosing_data = State()


async def change_minute(message: Message, state: FSMContext):
  print('hello1')
  await message.answer(
    text='Выберите, во сколько минут должно приходить сообщение:'
  )
  await state.set_state(InputTime.choosing_minutes)


async def add_minute(message: Message, state: FSMContext):
  await state.update_data(minute=message.text)
  data = await state.get_data()
  minutes = data['minute']
  await message.answer(f'Сообщения будут приходить каждую(ые) {minutes} минут(ы)')
  await state.set_state(None)


async def change_second(message: Message, state: FSMContext):
  print('hello')
  await message.answer(
    text='Выберите, во сколько секунд должно приходить сообщение:'
  )
  # await state.update_data(second=message.text)
  await state.set_state(InputTime.choosing_seconds)


async def add_second(message: Message, state: FSMContext):
  print('hello')
  await state.update_data(second=message.text)
  data = await state.get_data()
  seconds = data['second']
  await message.answer(f'Сообщения будут приходить каждую(ые) {seconds} секунд(ы)')
  await state.set_state(None)


async def print_hour(message: Message, state: FSMContext):
  await message.answer('Изменения приняты')
  await state.set_state(None)


async def incorrect_time(message: Message):
  await message.answer(
    text='Пожалуйста укажите число в диапазоне от 0 до 23'
  )

async def fetch_rss():
  choice = randint(0, 1)
  async with aiohttp.ClientSession() as session:
    if choice == 0:
      async with session.get(rss_url) as response:
        if response.status == 200:
          data = await response.text()
          return data
        else:
          return None
    else:
      async with session.get(rss_url1) as response:
        if response.status == 200:
          data = await response.text()
          return data
        else:
          return None


def parse_rss(data):
  root = ET.fromstring(data)
  items = root.findall('./channel/item')

  news = []
  news_titles = []
  title = ''
  item = random.choice(items)

  if not title in news_titles:
    link = item.find('link').text
    title = item.find('title').text
    news_titles.append(title)
    news.append({'title': title, 'link': link})
    return news
  else:
    fetch_rss()
    parse_rss(data)


async def send_news_to_chat(chat_id):
  data = await fetch_rss()
  if data:
    news = parse_rss(data)
    for entry in news:
      text = f"<b>{entry['title']}</b>\n{entry['link']}"
      await bot.send_message(chat_id, text, parse_mode=ParseMode.HTML)


async def cmd_start(message: Message, state: FSMContext):
  await message.answer(f'Здравствуйте! Выберите тип прихода сообщений: интервал или расписание:')
  await state.set_state(InputTime.choosing_data)


async def change_data(message: Message, state: FSMContext):
  await state.update_data(change=message.text)
  data = await state.get_data()
  change = data['change']
  await message.answer(f'Выбран тип: {change}')
  await state.set_state(None)


async def cmd_set_interval(message: Message, state: FSMContext):
  get_data = await state.get_data()

  scheduler = AsyncIOScheduler()

  if get_data['change'] == 'интервал':
    seconds = int(get_data['second'])
    minutes = int(get_data['minute'])

    scheduler.add_job(send_news_to_chat, trigger='interval', minutes=minutes, seconds=seconds, start_date=datetime.now(), kwargs={
        'chat_id': message.chat.id
      })

    await message.answer(f'Сообщения будут приходить с интервалом\n<b>{minutes} минут, {seconds} секунд</b>', parse_mode=ParseMode.HTML)
  else:
    scheduler.add_job(send_news_to_chat, trigger='cron', hour=2, minute=4, second=40, start_date=datetime.now(), kwargs={
                        'chat_id': message.chat.id
                      })

  scheduler.start()
  await state.set_state(None)


def register_states_handler(router: Router):
  pass
