import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Главное меню ---
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("🏗 Строительное оборудование"),
    KeyboardButton("🧱 Строительные материалы")
)
main_menu.add(
    KeyboardButton("👷 Строители"),
    KeyboardButton("📋 Вакансии")
)
main_menu.add(
    KeyboardButton("📑 Подряды и тендеры"),
    KeyboardButton("🚛 Грузоперевозки")
)
main_menu.add(
    KeyboardButton("🚜 Спецтехника"),
    KeyboardButton("➕ Опубликовать объявление")
)

# --- Обработчики ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(
        "Добро пожаловать в Союз Строителей и Поставщиков!\n"
        "Выберите категорию из меню:",
        reply_markup=main_menu
    )

@dp.message_handler(lambda m: m.text == "➕ Опубликовать объявление")
async def publish_ad(message: types.Message):
    await message.answer(
        "Отправьте текст вашего объявления.\n\n"
        "Формат:\nКатегория\nОписание\nКонтакты"
    )

@dp.message_handler(lambda m: m.text in [
    "🏗 Строительное оборудование",
    "🧱 Строительные материалы",
    "👷 Строители",
    "📋 Вакансии",
    "📑 Подряды и тендеры",
    "🚛 Грузоперевозки",
    "🚜 Спецтехника"
])
async def category_selected(message: types.Message):
    await message.answer(
        f"Вы выбрали категорию: {message.text}\n"
        f"Здесь будут объявления по этой теме."
    )

@dp.message_handler(content_types=["text"])
async def handle_text(message: types.Message):
    await message.answer("Ваше сообщение сохранено как объявление (пока без базы данных).")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
