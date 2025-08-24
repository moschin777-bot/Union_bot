from pyrogram import Client, filters

app = Client("union_bot")

@app.on_message(filters.text | filters.edited_message)
async def handler(client, message):
    await message.reply("Бот работает корректно!")

app.run()
