from aiogram import types, Dispatcher

from create_bot import bot, dp
from keyboards import keyboard_client

import json


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
        if str(message.from_user.id) not in users.keys():
            users[str(message.from_user.id)] = {}
            users[str(message.from_user.id)]["city"] = "Киев"
            users[str(message.from_user.id)]["notification"] = False

    with open('users.json', 'w', encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

    await message.answer(f"Hello, {message.from_user.first_name}! I am a Weather Bot\n"
                         f'🔸 ' "I can tell the current weather. Type /now or press button\n"
                         f'🔸 ' "I can describe the weather for today. Type /today or press button\n"
                         f'🔸 ' "I can predict the weather for 3 days. Type /3days or press button\n"
                         f'🔸 ' "I can try to guess the weather for 7 days. Type /7days or press button\n\n"
                         f"Your current city is {users[str(message.from_user.id)]['city']}.\n"
                         f"Type /city to change it or press button",
                         reply_markup=keyboard_client.main_keyboard)


# @dp.message_handler(commands=['settings'])
# @dp.message_handler(lambda message: message.text == "Settings")
async def set_new_notifications(message: types.Message):
    await message.answer(f"Ok, what do you want to change?",
                         reply_markup=keyboard_client.settings_keyboard)


# @dp.message_handler(content_types=['voice'])
async def voice(message: types.Message):
    await bot.send_voice(chat_id=message.chat.id, voice=message.voice.file_id)
    # TODO: send voice answer with "I would like to speak with you, but I don't want"
    # file_id = message.voice.file_id
    # file = await bot.get_file(file_id)
    # file_path = file.file_path
    # await bot.download_file(file_path, "Answer.mp3")


# @dp.message_handler()
async def common_message(message: types.Message):
    await message.answer(f"Sorry, i don't understand you. Try use keyboard\n",
                         reply_markup=keyboard_client.main_keyboard)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(set_new_notifications, commands=['settings'])
    dp.register_message_handler(set_new_notifications, lambda message: message.text == "Settings")

    dp.register_message_handler(voice, content_types=['voice'])

    dp.register_message_handler(common_message)
