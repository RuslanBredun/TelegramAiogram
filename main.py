from aiogram import executor

from create_bot import dp
from notifications import notification_time
from handlers import city_state_machine, settings_state_machine, common_handlers, weather_handlers

city_state_machine.register_handlers_city(dp)
settings_state_machine.register_handlers_settings(dp)
weather_handlers.register_handlers_weather(dp)
common_handlers.register_handlers_common(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=notification_time.on_startup)
