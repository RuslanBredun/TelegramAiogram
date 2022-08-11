import json
from create_bot import bot

from GismetToBot import get_now_weather
import asyncio
import aioschedule


async def notification():
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)

    for user in users:
        if users[user]['notification']:
            weather_right_now = get_now_weather(users[user]['city'])

            message = (f"🔸 Hello\n"
                       f"🔸 The weather in {users[user]['city']} at {weather_right_now['time']}\n"
                       f"🔸 The temperature is now {weather_right_now['temp']} degrees, "
                       f"although it feels like {weather_right_now['temp_sens']}\n"
                       f"🔸 The pressure is {weather_right_now['pressure']} mm and "
                       f"humidity is approximately {weather_right_now['humidity']}%\n"
                       f"🔸 The current wind speed is about {weather_right_now['wind']} m/s.\n"
                       f"🔸 Precipitation chance is {weather_right_now['precipitation']}%\n\n"
                       f"🔸 Sunrise time is {weather_right_now['sunrise_time']}\n"
                       f"🔸 Sunset time is {weather_right_now['sunset_time']}")

            await bot.send_message(chat_id=user, text=message)


async def scheduler(time):
    aioschedule.every().day.at(time).do(notification)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)


async def on_startup(_):
    time = "10:00"
    print(f"Time for notifications is {time} o'clock")
    asyncio.create_task(scheduler(time))
