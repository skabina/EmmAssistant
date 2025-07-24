import datetime
from zoneinfo import ZoneInfo
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes  
from telegram_client.utils import correct_email, greetings_by_time


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    current_time = datetime.datetime.now().time()
    await update.message.reply_text(greetings_by_time(current_time))

    keyboard = [
        [InlineKeyboardButton("Зареєструватися", callback_data='register_step')],
        [InlineKeyboardButton("Ввійти", callback_data='login_handle')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Щоб продовжити виберіть кнопку.", reply_markup=reply_markup)
    

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'register_step':
        context.user_data['register_step'] = 1
        await query.message.reply_text("Введіть вашу почту для реєстрації:")
    elif query.data == 'login_handle':
        context.user_data['login_handle'] = 1
        await query.message.reply_text("Введіть вашу почту:")
        

async def handle_register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    step = context.user_data.get('register_step', 0)
    user_message = update.message.text
    
    if step == 1:
        if correct_email(user_message):
            context.user_data['email'] = user_message
            context.user_data['register_step'] = 2
            await update.message.reply_text("Введіть пароль:")
        else: 
            await update.message.reply_text("Невірний формат почти, спробуйте ще раз:")
    elif step == 2:
        context.user_data['password'] = update.message.text
        context.user_data['register_step'] = 3
        await update.message.reply_text("https://support.google.com/accounts/answer/185833?hl=uk")
        await update.message.reply_text("⬆ Створіть пароль для малозахищених програм ⬆")
    elif step == 3:
        context.user_data['program_password'] = update.message.text
        await update.message.reply_text("Введіть пароль який створили:")    

