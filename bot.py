import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f'Привет, {user_name}! 👋\n'
        f'Я работаю 24/7 на Railway! 🚀\n'
        f'Напиши мне что-нибудь!'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        'Доступные команды:\n'
        '/start - Начать работу\n'
        '/help - Показать это сообщение\n\n'
        'Просто напиши мне текст, и я отвечу!'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Эхо-обработчик сообщений"""
    await update.message.reply_text(f'Вы написали: {update.message.text}')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f'Произошла ошибка: {context.error}')

def main():
    """Запуск бота"""
    if not TOKEN:
        logger.error("ОШИБКА: Токен не найден! Установите переменную TELEGRAM_BOT_TOKEN")
        return
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    logger.info("🤖 Бот успешно запущен!")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()
