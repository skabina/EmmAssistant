import asyncio
import uvicorn
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from config import settings
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler,  filters
from telegram_client.bot_handler import start, button, handle_register, all_date_user, menu
from database import db_helper

def main():
    app = ApplicationBuilder().token(settings.env.BOT_TOKEN).build()  
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("all_date_user", all_date_user))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_register))
    
    app.add_handler(CommandHandler("menu", menu))

    app.run_polling() 

    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()

