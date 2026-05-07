import os
import json
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Инициализация
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

# Промпт для анализа кода
CODE_ANALYSIS_PROMPT = """
Ты - AI ассистент для платформы Betking DX. 
Анализируй предоставленный код и напиши интересную новость/статью для Telegram канала.

Требования:
- Язык: Русский
- Формат: Профессиональный с эмодзи
- Длина: 200-400 символов
- Включи: что изменилось, почему это важно, какие преимущества

Код для анализа:
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start"""
    await update.message.reply_text(
        "🤖 **Betking DX AI News Bot**\n\n"
        "Отправьте мне код, и я создам новость для вашего канала!\n\n"
        "Команды:\n"
        "/start - Начать\n"
        "/help - Справка\n"
        "/analyze - Проанализировать код"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /help"""
    await update.message.reply_text(
        "📖 **Как использовать бота:**\n\n"
        "1️⃣ Отправьте мне код (JavaScript, Python и т.д.)\n"
        "2️⃣ Я проанализирую код на основе AI\n"
        "3️⃣ Получите готовую новость для Telegram\n\n"
        "💡 Пример: отправьте содержимое app.js"
    )

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка кода от пользователя"""
    code_text = update.message.text
    
    # Проверка длины кода
    if len(code_text) < 20:
        await update.message.reply_text("❌ Код слишком короткий. Отправьте полный код.")
        return
    
    # Сообщение о обработке
    processing_msg = await update.message.reply_text("⏳ Анализирую код...")
    
    try:
        # Запрос к Gemini
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=CODE_ANALYSIS_PROMPT + code_text + "\n\nНаписать новость на русском."
        )
        
        news_text = response.text
        
        # Редактируем сообщение с результатом
        await processing_msg.edit_text(
            f"✅ **Готовая новость:**\n\n{news_text}\n\n"
            f"📋 *Скопируйте текст и опубликуйте в канале*"
        )
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ Ошибка анализа: {str(e)}")

async def main() -> None:
    """Запуск бота"""
    if not TELEGRAM_TOKEN or not GOOGLE_API_KEY:
        raise ValueError("❌ Установите переменные окружения: TELEGRAM_BOT_TOKEN и GOOGLE_GENAI_API_KEY")
    
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Обработчик всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    
    # Запуск бота
    print("🚀 Бот запущен...")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
