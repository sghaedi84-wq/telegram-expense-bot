import os
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling
import pandas as pd

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# فایل اکسل برای ذخیره
EXCEL_FILE = "expenses.xlsx"

# اگر فایل وجود ندارد بساز
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["تاریخ", "مبلغ", "توضیحات"])
    df.to_excel(EXCEL_FILE, index=False)

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text.strip()
    
    try:
        # انتظار داریم فرمت: مبلغ توضیحات
        parts = text.split(" ", 1)
        amount = float(parts[0].replace(",", ""))
        note = parts[1] if len(parts) > 1 else "-"
        
        # تاریخ شمسی ساده با datetime
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # ذخیره در اکسل
        df = pd.read_excel(EXCEL_FILE)
        df = df.append({"تاریخ": date, "مبلغ": amount, "توضیحات": note}, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        
        await message.reply(f"ثبت شد ✅\nمبلغ: {amount}\nتوضیح: {note}")
    except Exception as e:
        await message.reply("فرمت پیام درست نیست. لطفا مثل:\n25000 قهوه")

# دستور برای گرفتن فایل اکسل
@dp.message_handler(commands=["getexcel"])
async def send_excel(message: types.Message):
    await message.reply_document(open(EXCEL_FILE, "rb"))

if __name__ == "__main__":
    start_polling(dp, skip_updates=True)
