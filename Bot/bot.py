import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# --- Настройка логирования ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Импорт токена ---
from config import BOT_TOKEN

# --- Обработчик /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "Пользователь"
    await update.message.reply_text(f"Привет, {user_name}! Отправь мне фото — и я его сохраню.")
    logger.info(f"Пользователь {update.effective_user.id} начал диалог.")

# --- Обработчик фото ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        photo = update.message.photo[-1]  # самое качественное фото
        photo_file = await photo.get_file()

        # Сохраняем фото
        file_path = f"{chat_id}_photo.jpg"
        await photo_file.download_to_drive(file_path)

        logger.info(f"Получено фото от пользователя {chat_id}")
        await update.message.reply_text("Фото получено!")

    except Exception as e:
        logger.error(f"Ошибка при обработке фото: {e}")
        await update.message.reply_text("Произошла ошибка при сохранении фото.")

# --- Запуск бота ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info("🤖 Бот запущен и готов к работе.")
    application.run_polling()