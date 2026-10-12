import os
from groq import Groq
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram.request import HTTPXRequest

# گرفتن توکن‌ها از Secrets
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# کلاینت Groq
groq_client = Groq(api_key=GROQ_API_KEY)

# پرامپت سیستمی
SYSTEM_PROMPT = """You are "Mohon's Soul" — Mohon's AI assistant on Telegram.
You reply to first-time senders only.

Tone: warm, short, human. Same language as sender. Max 2-3 lines.

NEVER ask "چطور میتونم کمکت کنم؟"

ALWAYS say something like:
"اگه دیر جواب دادم ناراحت نشی 🙏"

Sample (Persian):
سلام، خوش اومدی 🌿
من روح Mohon هستم، پیامت رو نگه میدارم تا خودش ببینه.
اگه دیر جواب داد ناراحت نشی 🙏 راحت باش بنویس."""

async def reply(update, context):
    user_message = update.message.text
    
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )
    
    await update.message.reply_text(response.choices[0].message.content)

# ساخت درخواست با تنظیمات ضد ReadError
request = HTTPXRequest(
    connection_pool_size=1,
    connect_timeout=30.0,
    read_timeout=30.0
)

# ساخت اپلیکیشن
app = ApplicationBuilder().token(TOKEN).get_updates_request(request).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

if __name__ == "__main__":
    app.run_polling()
