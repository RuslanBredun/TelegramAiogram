from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext

from create_bot import CitySM
from GismetToBot import get_html_code
from keyboards import keyboard_client

import json


# @dp.message_handler(commands=['city'])
# @dp.message_handler(lambda message: message.text == "Change city", state=None)
async def change_new_city(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
    await CitySM.city.set()
    await message.answer(f"Your current city is {users[str(message.from_user.id)]['city']}."
                         f"Enter your new city or type /cancel for canceling",
                         reply_markup=keyboard_client.city_keyboard)


# @dp.message_handler(lambda message: message.text == "cancel", state=CitySM.city)
# @dp.message_handler(state=CitySM.city, commands=['cancel'])
async def cancel(message: types.Message, state=CitySM):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
    await message.answer(f"Ok, your current city is {users[str(message.from_user.id)]['city']}",
                         reply_markup=keyboard_client.main_keyboard)


# @dp.message_handler(content_types=['text'], state=CitySM.city)
async def change_city(message: types.Message, state=FSMContext):

    if not get_html_code(message.text):
        await CitySM.city.set()
        await message.answer(f"Sorry, I can't find {message.text}."
                             f"Please, enter another city",
                             reply_markup=keyboard_client.city_keyboard)
    else:
        with open('users.json', 'r', encoding="utf-8") as file:
            users = json.load(file)
            users[str(message.from_user.id)]['city'] = message.text

        with open('users.json', 'w', encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=4)
        await message.answer(f"Ok, your current city is {users[str(message.from_user.id)]['city']}",
                             reply_markup=keyboard_client.main_keyboard)
        await state.finish()


def register_handlers_city(dp: Dispatcher):
    dp.register_message_handler(change_new_city,  commands=['city'])
    dp.register_message_handler(change_new_city, lambda message: message.text == "Change city", state=None)

    dp.register_message_handler(cancel, commands=['cancel'], state=CitySM.city)
    dp.register_message_handler(cancel, lambda message: message.text == "cancel", state=CitySM.city)

    dp.register_message_handler(change_city,  content_types=['text'], state=CitySM.city)
