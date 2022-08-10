from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_keyboard.add(KeyboardButton(text=f"Weather just now"),
                  KeyboardButton(text=f"Weather today"),
                  KeyboardButton(text=f"Weather 3 days"),
                  KeyboardButton(text=f"Weather 7 days"),
                  KeyboardButton(text=f"Settings"))

settings_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
settings_keyboard.add(KeyboardButton(text=f"Change city"),
                      KeyboardButton(text=f"Notifications"))

notifications_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
notifications_keyboard.add(KeyboardButton(text=f"Yes"),
                           KeyboardButton(text=f"No"))

city_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
city_keyboard.add(KeyboardButton(text=f"Киев"),
                  KeyboardButton(text=f"Харьков"),
                  KeyboardButton(text=f"Львов"),
                  KeyboardButton(text=f"Днепр"),
                  KeyboardButton(text=f"Одесса"),
                  KeyboardButton(text=f"Донецк"))
