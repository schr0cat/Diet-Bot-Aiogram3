import logging
import xml.etree.ElementTree as ET
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
import asyncio

API_TOKEN = '6811819685:AAFnLO4foxCj8DFgx3G0OQoA7O8GL2nTyz4'
RSS_URL = "https://habr.com/ru/rss/news/?fl=ru"

# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def fetch_rss():
    async with aiohttp.ClientSession() as session:
        async with session.get(RSS_URL) as response:
            if response.status == 200:
                data = await response.text()
                return data
            else:
                logging.error(f"Failed to fetch RSS feed: {response.status}")
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
            message = f"<b>{entry['title']}</b>\n{entry['link']}"
            await bot.send_message(chat_id, message)

@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: Message):
    await message.answer("Hi! I'm Habr News Bot.\nSend /news to get the latest news.")

@dp.message(Command(commands=["news"]))
async def send_news(message: Message):
    await send_news_to_chat(message.chat.id)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())