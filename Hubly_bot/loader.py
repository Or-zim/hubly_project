
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from django.conf import settings 
import os
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()