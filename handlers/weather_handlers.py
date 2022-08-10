from aiogram import types, md, Dispatcher

from GismetToBot import get_now_weather, get_today_weather, get_3d_weather, get_7d_weather

import json


# @dp.message_handler(commands=['now'])
# @dp.message_handler(lambda message: message.text == "Weather just now")
async def weather_now(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    weather_right_now = get_now_weather(users[str(message.from_user.id)]['city'])

    await message.answer(md.text(
        md.text(f'🔸', f"Hello, {message.from_user.first_name}!"),
        md.text(f'🔸', f"The weather in {users[str(message.from_user.id)]['city']} at {weather_right_now['time']}"),
        md.text(f'🔸', f"The temperature is now {weather_right_now['temp']} degrees, "
                f"although it feels like {weather_right_now['temp_sens']}"),
        md.text(f'🔸', f"The pressure is {weather_right_now['pressure']} mm and "
                f"humidity is approximately {weather_right_now['humidity']}%"),
        md.text(f'🔸', f"The current wind speed is about {weather_right_now['wind']} m/s."),
        md.text(f'🔸', f"Precipitation chance is {weather_right_now['precipitation']}%\n"),
        md.text(f'🔸', f"Sunrise time is {weather_right_now['sunrise_time']}"),
        md.text(f'🔸', f"Sunset time is {weather_right_now['sunset_time']}"),
        sep='\n'))


# @dp.message_handler(commands=['today'])
# @dp.message_handler(lambda message: message.text == "Weather today")
async def weather_today(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    weather_today = get_today_weather(users[str(message.from_user.id)]['city'])
    await message.answer(f"{weather_today}")


# @dp.message_handler(commands=['3days'])
# @dp.message_handler(lambda message: message.text == "Weather 3 days")
async def weather_3days(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    await message.answer(f"Collecting info. Wait, please...")
    weather_3days = get_3d_weather(users[str(message.from_user.id)]['city'])
    await message.answer(f"{weather_3days}")


# @dp.message_handler(commands=['7days'])
# @dp.message_handler(lambda message: message.text == "Weather 7 days")
async def weather_7days(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    await message.answer(f"Collecting info. Wait, please...")
    weather_7days = get_7d_weather(users[str(message.from_user.id)]['city'])
    await message.answer(f"{weather_7days}")


def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(weather_now, commands=['now'])
    dp.register_message_handler(weather_now, lambda message: message.text == "Weather just now")

    dp.register_message_handler(weather_today, commands=['today'])
    dp.register_message_handler(weather_today, lambda message: message.text == "Weather today")

    dp.register_message_handler(weather_3days, commands=['3days'])
    dp.register_message_handler(weather_3days, lambda message: message.text == "Weather 3 days")

    dp.register_message_handler(weather_7days, commands=['7days'])
    dp.register_message_handler(weather_7days, lambda message: message.text == "Weather 7 days")