
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Environment variable BOT_TOKEN is not set")

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# --- Keyboards ---
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Строительное оборудование"), KeyboardButton("Строительные материалы")],
        [KeyboardButton("Строители"), KeyboardButton("Вакансии")],
        [KeyboardButton("Подряды и тендеры"), KeyboardButton("Грузоперевозки")],
        [KeyboardButton("Спецтехника"), KeyboardButton("Опубликовать объявление")],
    ],
    resize_keyboard=True
)

@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    text = (
        "Добро пожаловать в Союз Строителей и Поставщиков!\n"
        "Выберите категорию из меню ниже или отправьте текст для публикации."
    )
    await message.answer(text, reply_markup=main_kb)

@dp.message_handler(lambda m: m.text == "Опубликовать объявление")
async def publish(message: types.Message):
    await message.answer(
        "Отправьте текст вашего объявления в формате:\n"
        "Категория\nОписание\nКонтакты"
    )

# echo for any other message (no 'edited' filters here)
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo(message: types.Message):
    await message.reply(f"Вы написали: {message.text}")

if __name__ == "__main__":
    print("Bot is starting...")
    executor.start_polling(dp, skip_updates=True)
