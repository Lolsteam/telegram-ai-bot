import os
from telegram.ext import ApplicationBuilder
from handlers import start

# Получаем токен из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден! Убедись, что вставил его в Variables Railway.")

# Создаем приложение бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Регистрируем обработчики команд
app.add_handler(start)

# Запуск бота
print("Бот запущен...")
app.run_polling()
