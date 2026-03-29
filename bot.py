import os
import asyncio
import logging

# SSL va Tarmoq xatoliklarini chetlab o'tish uchun maxsus sozlamalar
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile

# --- SOZLAMALAR ---
TOKEN = "8518747790:AAGUwBXsnNaN5obc3E8xOQVhFt1gh158A-o"
ADMIN_NAME = "Qosimov Alixon Alimovich"

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# --- ASOSIY MENYU ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💻 Windows o'rnatish (Format)")],
        [KeyboardButton(text="📞 Biz bilan bog'lanish")]
    ],
    resize_keyboard=True
)

# --- START HANDLER ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Rasm yo'lini tekshiramiz
    path = "profile.jpg"
    
    if os.path.exists(path):
        photo = FSInputFile(path)
        await message.answer_photo(
            photo=photo,
            caption=(
                f"Assalomu alaykum, {message.from_user.full_name}!\n"
                f"**{ADMIN_NAME}** - Kompyuter xizmatlari botiga xush kelibsiz.\n\n"
                "Kerakli xizmatni tanlang:"
            ),
            reply_markup=main_menu,
            parse_mode="Markdown"
        )
    else:
        # Agar rasm topilmasa, bot to'xtab qolmasligi uchun faqat matn yuboradi
        await message.answer(
            f"Assalomu alaykum! Rasm fayli topilmadi, lekin bot ishlashga tayyor.\n\n"
            f"Mutaxassis: {ADMIN_NAME}",
            reply_markup=main_menu
        )

# --- ALOQA HANDLER ---
@dp.message(F.text == "📞 Biz bilan bog'lanish")
async def contact_info(message: types.Message):
    await message.answer(
        f"👤 Mutaxassis: {ADMIN_NAME}\n"
        f"📞 Tel: +998 91 516 32 88\n"
        f"🎓 Termiz davlat universiteti talabasi"
    )

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())