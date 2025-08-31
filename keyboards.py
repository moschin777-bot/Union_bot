from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🛠 Оборудование'),KeyboardButton(text='🧱 Материалы')],
        [KeyboardButton(text='👷 Вакансии'),KeyboardButton(text='📑 Подряды/Тендеры')],
        [KeyboardButton(text='🚚 Перевозки'),KeyboardButton(text='🚜 Спецтехника')],
        [KeyboardButton(text='➕ Заявка'),KeyboardButton(text='👤 Личный кабинет')],
    ],resize_keyboard=True)

def unions_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='СОЮЗ ПОСТАВЩИКОВ',callback_data='union:suppliers')],
        [InlineKeyboardButton(text='СОЮЗ СТРОИТЕЛЕЙ',callback_data='union:builders')],
        [InlineKeyboardButton(text='СОЮЗ ПОДРЯДЧИКОВ',callback_data='union:contractors')],
        [InlineKeyboardButton(text='СОЮЗ ТЕНДЕРОВ',callback_data='union:tenders')],
        [InlineKeyboardButton(text='СОЮЗ СПЕЦТЕХНИКИ',callback_data='union:machines')],
        [InlineKeyboardButton(text='СОЮЗ ГРУЗОПЕРЕВОЗЧИКОВ',callback_data='union:logistics')],
        [InlineKeyboardButton(text='СОЮЗ АРЕНДОДАТЕЛЕЙ',callback_data='union:rent')],
    ])
