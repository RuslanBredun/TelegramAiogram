from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext

from create_bot import NotificationsSM
from keyboards import keyboard_client

import json


# @dp.message_handler(commands=['notifications'])
# @dp.message_handler(lambda message: message.text == "Set notification time", state=None)
async def set_notifications(message: types.Message):
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
    await NotificationsSM.notification.set()
    await message.answer(f"Currently you "
                         f"{'receive' if users[str(message.from_user.id)]['notification'] else 'dont receive'} "
                         f"notifications. "
                         f"Do you want to receive notifications?",
                         reply_markup=keyboard_client.notifications_keyboard)


# @dp.message_handler(lambda message: message.text == "cancel", state=NotificationsSM.notifications_time)
# @dp.message_handler(state=NotificationsSM.notifications_time, commands=['cancel'])
async def cancel(message: types.Message, state=NotificationsSM):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    with open('users.json', 'r', encoding="utf-8") as file:
        users = json.load(file)
    await message.answer(f"Ok will "
                         f"{'receiving' if users[str(message.from_user.id)]['notification'] else 'not receiving'} "
                         f"notifications.",
                         reply_markup=keyboard_client.main_keyboard)


# @dp.message_handler(content_types=['text'], state=NotificationsSM.notifications_time)
async def change_settings(message: types.Message, state=FSMContext):
    if message.text in ["Yes", "No"]:
        with open('users.json', 'r', encoding="utf-8") as file:
            users = json.load(file)

        if message.text == "Yes":
            users[str(message.from_user.id)]['notification'] = True
            await message.answer(f"Ok, you will receiving notifications at 10:00 every day",
                                 reply_markup=keyboard_client.main_keyboard)
        else:
            users[str(message.from_user.id)]['notification'] = False
            await message.answer(f"Ok, you will not receiving notifications",
                                 reply_markup=keyboard_client.main_keyboard)

        with open('users.json', 'w', encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=4)

        await state.finish()
    else:
        await NotificationsSM.notification.set()
        await message.answer(f"Sorry, not correct format."
                             f"Please, enter new notification time in correct format",
                             reply_markup=keyboard_client.notifications_keyboard)


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(set_notifications, commands=['notifications'])
    dp.register_message_handler(set_notifications, lambda message: message.text == "Notifications", state=None)

    dp.register_message_handler(cancel, lambda message: message.text == "cancel", state=NotificationsSM.notification)
    dp.register_message_handler(cancel,  state=NotificationsSM.notification, commands=['cancel'])

    dp.register_message_handler(change_settings, content_types=['text'], state=NotificationsSM.notification)


