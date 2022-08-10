import os
from aiogram import Bot, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=os.getenv(key="API_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class CitySM(StatesGroup):
    city = State()


class NotificationsSM(StatesGroup):
    notification = State()
