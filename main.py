import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_message(message: types.Message):
    await message.reply(f"پیام دریافت شد:\n{message.text}")

if __name__ == "__main__":
    start_polling(dp, skip_updates=True)
