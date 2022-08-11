from aiogram import types, Dispatcher

from GismetToBot import get_now_weather, get_today_weather, get_3d_weather, get_7d_weather

import json


# @dp.message_handler(commands=['now'])
# @dp.message_handler(lambda message: message.text == "Weather just now")
async def weather_now(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    weather_right_now = get_now_weather(users[str(message.from_user.id)]['city'])

    # TODO: create different messages that can be set in the settings
    await message.answer(f"🔸 Hello, {message.from_user.first_name}!\n"
                         f"🔸 The weather in {users[str(message.from_user.id)]['city']} at {weather_right_now['time']}\n"
                         f"🔸 The temperature is now {weather_right_now['temp']}, \n"
                         f"although it feels like {weather_right_now['temp_sens']}\n"
                         f"🔸 The pressure is {weather_right_now['pressure']} mm and \n"
                         f"humidity is approximately {weather_right_now['humidity']}%\n"
                         f"🔸 The current wind speed is about {weather_right_now['wind']} m/s.\n"
                         f"🔸 Precipitation chance is {weather_right_now['precipitation']}%\n\n"
                         f"🔸 Sunrise time is {weather_right_now['sunrise_time']}\n"
                         f"🔸 Sunset time is {weather_right_now['sunset_time']}\n")


# @dp.message_handler(commands=['today'])
# @dp.message_handler(lambda message: message.text == "Weather today")
async def weather_today(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    today_weather = get_today_weather(users[str(message.from_user.id)]['city'])

    # TODO: create different messages that can be set in the settings
    await message.answer(f"🔸 Hello, {message.from_user.first_name}!\n"
                         f"🔸 The weather in {users[str(message.from_user.id)]['city']} today:\n"
                         f"🔸 The temperature today will bo from {today_weather['min_temp']} to "
                         f"{today_weather['max_temp']}, "
                         f"although it feels like {today_weather['min_temp_sense']}-"
                         f"{today_weather['max_temp_sense']}"
                         f"🔸 The pressure is {today_weather['pressure']} mm and \n"
                         f"humidity is approximately {today_weather['min_humidity']} - "
                         f"{today_weather['max_humidity']}%\n"
                         f"🔸 The current wind speed is about {today_weather['min_wind']} - "
                         f"{today_weather['max_wind']} m/s.\n"
                         f"🔸 Precipitation chance is {today_weather['max_precipitation']}%")


# @dp.message_handler(commands=['3days'])
# @dp.message_handler(lambda message: message.text == "Weather 3 days")
async def weather_3days(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    await message.answer(f"🔸 Hello, {message.from_user.first_name}! Collecting info. Wait, please...")
    days3_weather = get_3d_weather(users[str(message.from_user.id)]['city'])

    # TODO: create different messages that can be set in the settings
    for day in days3_weather:
        await message.answer(f"{day['day']} \n"
                             f"🔸 The temperature will bo from {day['min_temp']} to "
                             f"{day['max_temp']}C\n"
                             f"🔸 {day['description']}")


# @dp.message_handler(commands=['7days'])
# @dp.message_handler(lambda message: message.text == "Weather 7 days")
async def weather_7days(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    await message.answer(f"🔸 Hello, {message.from_user.first_name}! Collecting info. Wait, please...")
    days7_weather = get_7d_weather(users[str(message.from_user.id)]['city'])

    # TODO: create different messages that can be set in the settings
    for day in days7_weather:
        await message.answer(f"{day['day']} \n"
                             f"🔸 The temperature will bo from {day['min_temp']} to "
                             f"{day['max_temp']}\n"
                             f"🔸 {day['description']}")


def register_handlers_weather(dp: Dispatcher):
    dp.register_message_handler(weather_now, commands=['now'])
    dp.register_message_handler(weather_now, lambda message: message.text == "Weather just now")

    dp.register_message_handler(weather_today, commands=['today'])
    dp.register_message_handler(weather_today, lambda message: message.text == "Weather today")

    dp.register_message_handler(weather_3days, commands=['3days'])
    dp.register_message_handler(weather_3days, lambda message: message.text == "Weather 3 days")

    dp.register_message_handler(weather_7days, commands=['7days'])
    dp.register_message_handler(weather_7days, lambda message: message.text == "Weather 7 days")