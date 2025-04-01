import os
import logging
import asyncio
import time
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest, TelegramUnauthorizedError

# .env faylidan sozlamalarni yuklash
load_dotenv()

# TOKENNI TO'G'RI O'QISH (o'zgartirildi)
BOT_TOKEN = "8121896700:AAEWeWVsX6qWqLx5pIt4K9_YZPLJwUBFQ3U"  # Token to'g'ridan berilgan
CHANNEL_USERNAME = "@Qurbonoff_channel"  # Kanal username (o'zgartirildi)
ADMIN_ID = 5829043831  # Admin ID (o'zgartirildi)

# Log sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename='bot.log'
)
logger = logging.getLogger(__name__)

# Bot va Dispatcher
bot = Bot(
    token=BOT_TOKEN,  # Token to'g'ridan ishlatilmoqda
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Kino ma'lumotlari bazasi
movies_db = {
    "?": {"title": "#Mundarijalar", "link": "https://t.me/Kinolar_Mundarejasi/3"},
    "1": {"title": "Burama Metal", "link": "https://t.me/Siz_Izlagan_Filmlar/10"},
    "2": {"title": "MEGAN", "link": "https://t.me/Siz_Izlagan_Filmlar/21"},
    "3": {"title": "Tug'ilmagan", "link": "https://t.me/Siz_Izlagan_Filmlar/22"},
    "4": {"title": "Sakkizoyoq o’yini", "link": "https://t.me/Siz_Izlagan_Filmlar/23"},
    "5": {"title": "Morgdagi Qotillik", "link": "https://t.me/Siz_Izlagan_Filmlar/24"},
    "6": {"title": "Overlord", "link": "https://t.me/Siz_Izlagan_Filmlar/25"},
    "7": {"title": "Yengilmas 1", "link": "https://t.me/Siz_Izlagan_Filmlar/30"},
    "8": {"title": "Yengilmas 2", "link": "https://t.me/Siz_Izlagan_Filmlar/31"},
    "9": {"title": "Yengilmas 3", "link": "https://t.me/Siz_Izlagan_Filmlar/32"},
    "10": {"title": "Yengilmas 4", "link": "https://t.me/Siz_Izlagan_Filmlar/33"},
    "11": {"title": "O’lim kuni muborak", "link": "https://t.me/Siz_Izlagan_Filmlar/34"},
    "12": {"title": "O’lim kuni muborak 2", "link": "https://t.me/Siz_Izlagan_Filmlar/35"},
    "13": {"title": "Hellboy", "link": "https://t.me/Siz_Izlagan_Filmlar/36"},
    "14": {"title": "Chappi", "link": "https://t.me/Siz_Izlagan_Filmlar/37"},
    "15": {"title": "G’aroyib odamlar: Rassamaxa", "link": "https://t.me/Siz_Izlagan_Filmlar/38"},
    "16": {"title": "Joker", "link": "https://t.me/Siz_Izlagan_Filmlar/39"},
    "17": {"title": "Vampir", "link": "https://t.me/Siz_Izlagan_Filmlar/40"},
    "18": {"title": "Texasdagi qonli qirg’in", "link": "https://t.me/Siz_Izlagan_Filmlar/41"},
    "19": {"title": "Epidemiya", "link": "https://t.me/Siz_Izlagan_Filmlar/42"},
    "20": {"title": "Piraniyalar 1", "link": "https://t.me/Siz_Izlagan_Filmlar/43"},
    "21": {"title": "Piraniyalar 2", "link": "https://t.me/Siz_Izlagan_Filmlar/44"},
    "22": {"title": "Tarot: O’lim kartasi", "link": "https://t.me/Siz_Izlagan_Filmlar/45"},
    "23": {"title": "Teskari Hisob", "link": "https://t.me/Siz_Izlagan_Filmlar/46"},
    "24": {"title": "Avram Linkoln: Vampir ovchisi", "link": "https://t.me/Siz_Izlagan_Filmlar/47"},
    "25": {"title": "Demetr: Shaytonning oxirgi sayoxati", "link": "https://t.me/Siz_Izlagan_Filmlar/48"},
    "26": {"title": "Narkoman Ayiq", "link": "https://t.me/Siz_Izlagan_Filmlar/49"},
    "27": {"title": "Vinniy pux: Qon va Asal", "link": "https://t.me/Siz_Izlagan_Filmlar/50"},
    "28": {"title": "Iblis qutisi", "link": "https://t.me/Siz_Izlagan_Filmlar/51"},
    "29": {"title": "Iblis qutisi 2", "link": "https://t.me/Siz_Izlagan_Filmlar/52"},
    "30": {"title": "O’lim daftari", "link": "https://t.me/Siz_Izlagan_Filmlar/53"},
    "31": {"title": "Qush qutisi | O’lim iskanjasida", "link": "https://t.me/Siz_Izlagan_Filmlar/54"},
    "32": {"title": "Qush qutisi 2 | O’lim iskanjasida 2", "link": "https://t.me/Siz_Izlagan_Filmlar/55"},
    "33": {"title": "Uddaburon yigitlar 4", "link": "https://t.me/Siz_Izlagan_Filmlar/56"},
    "34": {"title": "Dunyodan uzulgan", "link": "https://t.me/Siz_Izlagan_Filmlar/57"},
    "35": {"title": "Oilaviy reja", "link": "https://t.me/Siz_Izlagan_Filmlar/58"},
    "36": {"title": "Super dada", "link": "https://t.me/Siz_Izlagan_Filmlar/59"},
    "37": {"title": "Jinoyatchilar shaxri 4", "link": "https://t.me/Siz_Izlagan_Filmlar/60"},
    "38": {"title": "Lara Kroft: Daxma talonchisi", "link": "https://t.me/Siz_Izlagan_Filmlar/61"},
    "39": {"title": "Uchinchisi ortiqcha 1", "link": "https://t.me/Siz_Izlagan_Filmlar/62"},
    "40": {"title": "Uchinchisi ortiqcha 2", "link": "https://t.me/Siz_Izlagan_Filmlar/63"},
}


async def check_channel_subscription(user_id: int) -> bool:
    """Foydalanuvchi kanalga a'zo ekanligini tekshirish"""
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except (TelegramBadRequest, TelegramUnauthorizedError) as e:
        logger.error(f"Kanal tekshiruvida xato: {e}")
        return False


@dp.message(Command("start", "help"))
async def start_handler(message: types.Message):
    """Start komandasi uchun handler"""
    try:
        if not await check_channel_subscription(message.from_user.id):
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Kanalga a'zo bo'lish", url=f"https://t.me/Qurbonoff_channel")],
                [types.InlineKeyboardButton(text="✅ A'zolikni tekshirish", callback_data="check_sub")]
            ])
            await message.answer(
                "Botdan foydalanish uchun kanalimizga a'zo bo'ling!",
                reply_markup=keyboard
            )
            return

        await message.answer(
            "👋 Assalomu alaykum! Kino nomini yuboring.\n\n"
            "📌 Eslatma: Kino nomini bosh harflarda yozing!"
        )
    except Exception as e:
        logger.error(f"Start handlerda xato: {e}")
        await message.answer("⚠️ Botda vaqtinchalik xato yuz berdi. Iltimos, keyinroq urinib ko'ring.")


@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):
    """A'zolikni tekshirish tugmasi uchun handler"""
    try:
        if await check_channel_subscription(callback.from_user.id):
            await callback.message.edit_text(
                "✅ Rahmat! Endi kino nomini yuborishingiz mumkin. \n Kino nomini bosh harflarda yozing!",
                reply_markup=None
            )
        else:
            await callback.answer("❌ Siz hali kanalga a'zo bo'lmagansiz!", show_alert=True)
    except Exception as e:
        logger.error(f"Callback handlerda xato: {e}")
        await callback.answer("Xato yuz berdi. Iltimos, qayta urinib ko'ring.", show_alert=True)


@dp.message()
async def message_handler(message: types.Message):
    """Barcha xabarlar uchun handler"""
    try:
        if not await check_channel_subscription(message.from_user.id):
            return

        movie_code = message.text.strip()
        if movie_code in movies_db:
            movie = movies_db[movie_code]
            response = (
                f"🎬 <b>{movie['title']}</b>\n\n"
                f"🔗 <a href='{movie['link']}'>Ko'rish uchun link</a>\n\n"
            )
            await message.answer(response)
        else:
            await message.answer("⚠️ Noto'g'ri kino nomi. Qaytadan urinib ko'ring. \n Kino nomini bosh harflarda yozing!")
    except Exception as e:
        logger.error(f"Xabar handlerda xato: {e}")


async def main():
    """Asosiy dastur"""
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Bot ishga tushirishda xato: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logger.error(f"Bot qayta ishga tushirilmoqda. Xato: {e}")
            time.sleep(10)