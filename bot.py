import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def reply(update, context):
    await update.message.reply_text("جوابت رو اینجا بنویس")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

if __name__ == "__main__":
    app.run_polling()
