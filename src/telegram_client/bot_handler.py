import datetime
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram_client.utils import correct_email, greetings_by_time, escape_md,  random_answer_errors
from database import db_helper

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user_id = update.effective_user.id 
    current_time = datetime.datetime.now().time()

    if await db_helper.check_user(tg_user_id):
        await update.message.reply_text(greetings_by_time(current_time))
        await menu(update, context)     
    else:
        context.user_data['register_step'] = 1
        await update.message.reply_text("Розпочнемо реєстрацію😉")
        await update.message.reply_text("Введіть вашу 📧почту:")


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  

    if query.data == 'register_step':
        context.user_data['register_step'] = 1
        await update.message.reply_text("Розпочнемо реєстрацію😉")
        await update.message.reply_text("Введіть вашу 📧почту:")
    elif query.data == 'set_email_step':
        await query.edit_message_text("✉️ Введіть новий email:")        
        context.user_data['set_email_step'] = 1
    elif query.data == 'set_password_application_step':
        pass

    elif query.data == 'activate_is_step':
        pass
    else:
        await query.edit_message_text("Невідома дія 🤔")

async def register_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    step = context.user_data.get('register_step', 0)
    user_message = update.message.text.strip()

    if step == 1:
        if correct_email(user_message):
            context.user_data['email'] = user_message
            context.user_data['register_step'] = 2
            await update.message.reply_text("https://support.google.com/accounts/answer/185833?hl=uk")
            await update.message.reply_text("⬆ Створіть пароль для малозахищених програм та надішліть мені ⬆")
        else:
            await update.message.reply_text("Не вірний формат пошти. Спробуйте ще раз")
    elif step == 2:
        tg_user_id = update.effective_user.id
        context.user_data['tg_user_id'] = tg_user_id
        context.user_data['password_application'] = re.sub(r"\s+", "", user_message)

        await update.message.reply_text("Зберігаю дані ⏳")

        if not await db_helper.check_user(tg_user_id):
            await db_helper.register_user(
                tg_user_id,
                context.user_data['email'],
                context.user_data['password_application'],
                is_active=False
            )
            await update.message.reply_text("Готово✅ \nРозпочинаємо співпрацю ⏭")
            context.user_data['register_step'] = 0
            await menu(update, context)
    else:
        await handle_main_menu(update, context)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):   
    keyboard = [[KeyboardButton("📬 Мої дані"), 
                 KeyboardButton("⚙ Налаштування"),
                 KeyboardButton("📩 Почта")]
                ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Оберіть опцію:", reply_markup=reply_markup)

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.strip()

    if user_message == '📬 Мої дані':
        await show_date_user(update, context)
    elif user_message == '⚙ Налаштування':
        await settings(update, context)
    else:
        await update.message.reply_text(random_answer_errors())

async def editor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [
        [InlineKeyboardButton("📝 Email", callback_data='set_email_step')],
        [InlineKeyboardButton("🔐 Пароль", callback_data='set_password_application_step')],
        [InlineKeyboardButton("📌 Автоконтроль", callback_data='activate_is_step')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Виберіть які дані хочете змінити🗂", reply_markup=reply_markup)

async def set_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    step = context.user_data.get('set_email_step', 0)
    user_message = update.message.text.strip() 
    if step == 1:
        if correct_email(user_message):
            context.user_data['email'] = user_message
            context.user_data['set_email_step'] = 0
            await update.message.reply_text("📧 Email успішно оновлено")
        else:
            await update.message.reply_text("Не вірний формат пошти. Спробуйте ще раз")
    

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name

    await update.message.reply_text(f"{first_name}, твій профіль\n➖➖➖➖➖➖\n Змінити дані: /editor", parse_mode="MarkdownV2")
        
       
async def show_date_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tg_user_id = update.effective_user.id 
    if await db_helper.check_user(tg_user_id):
        date_user = await db_helper.get_user(tg_user_id)
 
        message = f"""Ось ваші дані:
            Telegram ID: {escape_md(str(date_user['tg_user_id']))}
            📧Email: {escape_md(date_user['email'])}
            🔑Пароль: ||{escape_md(date_user['password_application'])}||
            💌Повідомлення про новий лист: {"✅" if date_user['is_active'] else "❌"}
            """
        await update.message.reply_text(message, parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("Спершу зареєструйтеся‼") 
   