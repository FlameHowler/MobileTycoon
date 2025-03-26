import logging

from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BotCommand, MenuButtonWebApp, WebAppInfo
from aiogram.types import Message

router = Router()

# Токен бота (замени на свой)
TOKEN = "7188970581:AAFqdZjOxp5oU3rcYAixNYs2Wqs4OjjchI8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Минимальная логика бота
@router.message(Command("start"))
async def start_command(message: Message):
    await bot.set_my_commands([BotCommand(command="app", description="Открыть Mini App")])

    # Устанавливаем кнопку Mini App в меню
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="🚀 Открыть игру",
            web_app=WebAppInfo(url="https://mobiletycoon.onrender.com")  # Замените на свой URL!
        )
    )

    await message.answer("Привет! Нажми на кнопку в меню, чтобы открыть игру. 🚀")

# Функция запуска бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())