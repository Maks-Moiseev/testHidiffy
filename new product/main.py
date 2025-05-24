import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import json
from datetime import datetime

# ------------------- КОНФИГУРАЦИЯ -------------------
BOT_TOKEN = "8075652827:AAEgPlTxnGrO4NcZ2KXBSWSxe_t3uccJtq4"
API_URL = "https://45.82.15.213.sslip.io/MY32Nj607jUvh2m03VgBftn/api/v2/admin/user/"
API_KEY = "9aac422d-6819-4412-9fa7-a439ce308ca8"
SSL_VERIFY = True  # Отключить для самоподписанных сертификатов
# ----------------------------------------------------

# Настройка продвинутого логгирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def create_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создание пользователя с проверкой всех параметров"""
    try:
        # Проверка прав пользователя
        if update.message.from_user.id != 1102014206:  # Замените на ваш Telegram ID
            await update.message.reply_text("🚫 У вас нет прав для этой команды!")
            return

        # Генерация данных пользователя
        user_data = {
  "added_by_uuid": None,
  "comment": "fdghgh",
  "current_usage_GB": 0,
  "ed25519_private_key": "string",
  "ed25519_public_key": "string",
  "enable": True,
  "is_active": True,
  "lang": "ru",
  "last_online": None,
  "last_reset_time": None,
  "mode": "no_reset",
  "name": "string",
  "package_days": 10,
  "start_date": "2025-05-24",
  "telegram_id": 134250,
  "usage_limit_GB": 10,
  "uuid": None,
  "wg_pk": "string",
  "wg_psk": "string",
  "wg_pub": "string"
}

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Hiddify-API-Key": API_KEY
        }

        # Проверка доступности API
        if not await check_api_health(headers):
            await update.message.reply_text("🔴 API Hiddify недоступен!")
            return

        # Отправка запроса
        response = requests.post(
            API_URL,
            headers=headers,
            json=user_data,
            verify=SSL_VERIFY,
            timeout=15
        )

        # Обработка ответа
        if response.status_code == 200:
            result = response.json()
            await update.message.reply_text(
                f"✅ Успешно создан!\n"
                f"👤 Имя: {result.get('name', 'N/A')}\n"
                f"📊 Лимит: {result.get('usage_limit_GB', 0)} GB\n"
                f"📅 Действителен до: {result.get('expire_date', 'N/A')}\n"
                f"Ваш ключ: https://45.82.15.213.sslip.io/7uflOTGssTTc/{result.get('uuid', 'N/A')}/?home=true"
            )
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            await update.message.reply_text(
                f"❌ Ошибка API ({response.status_code})\n"
                f"{response.json().get('detail', 'Unknown error')}"
            )

    except Exception as e:
        logger.exception("Critical error in create_user:")
        await update.message.reply_text("🔥 Критическая ошибка! Проверьте логи.")

def generate_wg_psk():
    """Генерация WireGuard PSK ключа"""
    try:
        return os.urandom(32).hex()  # Простая генерация для примера
    except Exception as e:
        logger.warning(f"WG PSK generation failed: {str(e)}")
        return "default_psk_key"

async def check_api_health(headers):
    """Проверка работоспособности API"""
    try:
        test_url = API_URL.rsplit('/', 5)[0] + "/"
        response = requests.get(test_url, headers=headers, verify=SSL_VERIFY, timeout=100)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"API Health Check Failed: {str(e)}")
        return False

def main():
    # Инициализация бота
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация команд
    application.add_handler(CommandHandler("create_user", create_user))

    # Запуск
    logger.info("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()