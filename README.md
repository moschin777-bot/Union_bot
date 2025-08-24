
# Union Bot (aiogram)

Минимальный рабочий бот на aiogram v2. Требуется только переменная окружения `BOT_TOKEN`.

## Локальный запуск
```bash
pip install -r requirements.txt
export BOT_TOKEN=123456:ABC...
python bot.py
```

## Railway
- Variables: `BOT_TOKEN=<токен_бота>`
- Deploy: Procfile -> `worker: python bot.py`
