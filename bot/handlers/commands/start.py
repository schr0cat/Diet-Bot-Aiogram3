import asyncio
from datetime import datetime

from aiogram import types, Router, Bot
from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import aioschedule

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Any, Awaitable, Callable, Dict
import xml.etree.ElementTree as ET

from bot.utils.config_reader import config

rss_url = 'https://habr.com/ru/rss/news/?fl=ru'
bot = Bot(token=config.token)


async def fetch_rss():
  async with aiohttp.ClientSession() as session:
    async with session.get(rss_url) as response:
      if response.status == 200:
        data = await response.text()
        return data
      else:
        # logging.error(f"Failed to fetch RSS feed: {response.status}")
        return None


def parse_rss(data):
  root = ET.fromstring(data)
  items = root.findall('./channel/item')
  news = []
  for item in items[:5]:  # Берем последние 5 новостей
    title = item.find('title').text
    link = item.find('link').text
    news.append({'title': title, 'link': link})
  return news


async def send_news_to_chat(chat_id):
  data = await fetch_rss()
  if data:
    news = parse_rss(data)
    for entry in news:
      text = f"<b>{entry['title']}</b>\n{entry['link']}"
      await bot.send_message(chat_id, text)


async def cmd_start(message: Message):
  await message.answer('Hello')
  scheduler = AsyncIOScheduler()

  scheduler.add_job(send_news_to_chat, trigger='cron', hour=2, minute=41, start_date=datetime.now(), kwargs={
    'chat_id': message.chat.id
  })

  scheduler.start()


def register_states_handler(router: Router):
  router.callback_query.register(cmd_start)
