import os
from pyrogram import Client, filters
from keywords import keywords

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_api_hash")

app = Client("bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.text & ~filters.edited)
async def handle_message(client, message):
    text = message.text.lower()
    found = None

    for category, subcats in keywords.items():
        for subcat, words in subcats.items():
            for w in words:
                if w in text:
                    found = (category, subcat)
                    break
            if found:
                break
        if found:
            break

    if found:
        await message.reply(f"Объявление определено: {found[0]} → {found[1]}")
    else:
        await message.reply("Не удалось определить категорию. Уточните вручную.")

app.run()
