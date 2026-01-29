import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("привет. пиши мне или упоминай меня в группе")

async def ask_ai(text: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.lower()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.text or ""
    bot = context.bot
    me = await bot.get_me()

    should_reply = False

    if msg.chat.type == "private":
        should_reply = True

    if f"@{me.username.lower()}" in text.lower():
        should_reply = True

    if msg.reply_to_message and msg.reply_to_message.from_user.id == me.id:
        should_reply = True

    if not should_reply:
        return

    try:
        reply = await ask_ai(text)
    except:
        reply = "что-то пошло не так"

    await msg.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
