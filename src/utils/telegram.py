from os import getenv
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update)
    print(context)
    
    await update.message.reply_text(f'Hello {update.effective_user.first_name} in chat {context._chat_id}')



app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("hello", hello, block=False))


# app.run_polling()