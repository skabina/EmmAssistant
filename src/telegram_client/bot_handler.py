import datetime
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes  
from telegram_client.utils import correct_email, greetings_by_time
from database import db_helper

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    tg_user_id = update.effective_user.id 
    current_time = datetime.datetime.now().time()

    if await db_helper.check_user(tg_user_id):
            await update.message.reply_text(greetings_by_time(current_time)) 

            #Жоскі фічі   
    elif not await db_helper.check_user(tg_user_id):         
        
        await update.message.reply_text(greetings_by_time(current_time))

        keyboard = [    
            [InlineKeyboardButton("Зареєструватися", callback_data='register_step')],
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

            await update.message.reply_text("https://support.google.com/accounts/answer/185833?hl=uk")
            await update.message.reply_text("⬆ Створіть пароль для малозахищених програм та наділшість мені ⬆")
        else: 
            await update.message.reply_text("Невірний формат почти, спробуйте ще раз:")
    elif step == 2:
        tg_user_id = update.effective_user.id 
        context.user_data['tg_user_id'] = tg_user_id

        password_application = re.sub(r"\s+", "", update.message.text)
        context.user_data['password_application'] = password_application

        await update.message.reply_text("Зберігаю дані ♻") 

        is_active_default = False
        if not await db_helper.check_user(tg_user_id):
            await db_helper.register_user(context.user_data['tg_user_id'], context.user_data['email'], context.user_data['password_application'], is_active_default)
            await update.message.reply_text("Готово✅ Розпочинаємо співпрацю ⏭")
            date_user = await db_helper.get_user(tg_user_id)
            await update.message.reply_text("Ось ваші дані:\nВаш id: {date_user[tg_user_id]}\nВаша email")
            await db_helper.disconnect()
         

async def all_date_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        tg_user_id = update.effective_user.id 
        date_user = await db_helper.get_user(tg_user_id)

        message = f"""Ось ваші дані:
        Telegram ID: {date_user['tg_user_id']}
        📧Email: {date_user['email']}
        🔑Пароль: || {date_user['password_application']} ||
        💌Повідомлення про новий лист: {'✅' if date_user['is_active'] else '❌'}
        """
        message = message.replace(".", "\.")  
        await update.message.reply_text(message,parse_mode="MarkdownV2")
        
                
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📬 Мої дані"), KeyboardButton("⚙ Налаштування")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Оберіть опцію:", reply_markup=reply_markup)                
               
   


