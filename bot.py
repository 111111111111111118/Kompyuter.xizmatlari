import os, asyncio, logging, sqlite3, wikipedia
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from deep_translator import GoogleTranslator

# --- SOZLAMALAR ---
TOKEN = "8518747790:AAGUwBXsnNaN5obc3E8xOQVhFt1gh158A-o"
ADMIN_NAME, PHONE = "Alixon", "+998 91 516 32 88"
PROXY_URL = "http://proxy.server:3128"
wikipedia.set_lang("uz")

session = AiohttpSession(proxy=PROXY_URL)
bot, dp = Bot(token=TOKEN, session=session), Dispatcher()
logging.basicConfig(level=logging.INFO)

# --- BAZA ---
db = sqlite3.connect("users.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)")
db.commit()

# --- ASOSIY MENYU ---
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🛠 Xizmatlar"), KeyboardButton(text="📝 Buyurtma berish")],
    [KeyboardButton(text="🔍 Wikipedia"), KeyboardButton(text="🔤 Tarjimon")],
    [KeyboardButton(text="📍 Manzil"), KeyboardButton(text="📞 Bog'lanish")]
], resize_keyboard=True)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    cursor.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (message.from_user.id,))
    db.commit()
    text = f"Assalomu alaykum!\nAdmin: {ADMIN_NAME}\nTel: {PHONE}\n\nBo'limni tanlang:"
    path = "profile.jpg"
    if os.path.exists(path):
        await message.answer_photo(photo=FSInputFile(path), caption=text, reply_markup=main_menu)
    else:
        await message.answer(text, reply_markup=main_menu)

@dp.message(F.text == "🛠 Xizmatlar")
async def serv(m: types.Message): 
    await m.answer(f"🛠 **Xizmatlar:** Formatlash, Dasturlar, Ma'lumot tiklash.\n📞 Tel: {PHONE}", parse_mode="Markdown")

@dp.message(F.text == "📝 Buyurtma berish")
async def ord(m: types.Message): 
    await m.answer(f"📝 Buyurtma berish uchun qo'ng'iroq qiling:\n📞 **{PHONE}**", parse_mode="Markdown")

@dp.message(F.text == "📍 Manzil")
async def loc(m: types.Message): 
    await m.answer("📍 **Manzil:** Termiz shahri, Termiz Davlat Universiteti yaqinida.", parse_mode="Markdown")

# --- BOG'LANISH BO'LIMI (HAVOLALARSIZ, FAQAT TUGMALAR) ---
@dp.message(F.text == "📞 Bog'lanish")
async def cont(m: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Alixon (Asosiy)", url="https://t.me/+998915163288")],
        [InlineKeyboardButton(text="💬 Qo'shimcha aloqa", url="https://t.me/+998990730288")]
    ])
    await m.answer("📞 **Biz bilan bog'lanish uchun pastdagi tugmalarni tanlang:**", reply_markup=kb, parse_mode="Markdown")

@dp.message(F.text == "🔤 Tarjimon")
async def tr_i(m: types.Message): 
    await m.answer("🔤 Inglizcha so'z yoki gap yuboring, o'zbekchaga tarjima qilaman.")

@dp.message(F.text == "🔍 Wikipedia")
async def wk_i(m: types.Message): 
    await m.answer("🔍 Qidirmoqchi bo'lgan mavzuingizni yozing:")

@dp.message()
async def auto(m: types.Message):
    if m.text in ["🛠 Xizmatlar", "📝 Buyurtma berish", "🔍 Wikipedia", "🔤 Tarjimon", "📍 Manzil", "📞 Bog'lanish"]: return
    try:
        tr = GoogleTranslator(source='en', target='uz').translate(m.text)
        if tr.lower() != m.text.lower():
            await m.answer(f"🇺🇿 **Tarjima:** {tr}", parse_mode="Markdown")
        else:
            wk = wikipedia.summary(m.text, sentences=2)
            await m.answer(f"🔍 **Wikipedia:** {wk}", parse_mode="Markdown")
    except:
        await m.answer("❌ Ma'lumot topilmadi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
