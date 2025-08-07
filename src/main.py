import asyncio
from config import settings
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram_client.bot_handler import start, register_message, editor, set_email, handle_callback

def main():
    app = ApplicationBuilder().token(settings.env.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, register_message))
    app.add_handler(CommandHandler("editor", editor))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_email))
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.run_polling()

if __name__ == "__main__":
    main()
