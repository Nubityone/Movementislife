#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram бот для отправки мотивирующих цитат
Разработан для запуска через GitHub Actions или аналогичные сервисы
Поддерживает годовой цикл из 365 цитат
"""

import os
import sys
import logging
import datetime
import requests
from quotes import QUOTES

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Проверка наличия необходимых переменных окружения
if not TELEGRAM_BOT_TOKEN:
    logger.error("Не указан токен бота. Установите переменную окружения TELEGRAM_BOT_TOKEN")
    sys.exit(1)

if not CHAT_ID:
    logger.error("Не указан ID чата. Установите переменную окружения TELEGRAM_CHAT_ID")
    sys.exit(1)

def get_day_of_year():
    """
    Получает текущий день года (от 1 до 365/366)
    """
    today = datetime.datetime.now()
    return today.timetuple().tm_yday

def get_quote_for_today():
    """
    Получает цитату для текущего дня года
    """
    day_of_year = get_day_of_year()
    
    # Получаем индекс цитаты (от 0 до 364)
    # Если день года больше 365, используем остаток от деления
    quote_index = (day_of_year - 1) % len(QUOTES)
    
    return QUOTES[quote_index]

def format_quote(quote):
    """
    Форматирует цитату для отправки с эмодзи
    """
    emoji = quote.get('emoji', '')
    return f"{emoji} *{quote['text']}*\n\n— _{quote['author']}_"

def send_quote():
    """
    Отправляет сегодняшнюю цитату в указанный чат
    """
    quote = get_quote_for_today()
    formatted_quote = format_quote(quote)
    
    today = datetime.datetime.now().strftime("%d.%m.%Y")
    message = f"Доброе утро! ☀️ \n\n{formatted_quote}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logger.info(f"Цитата успешно отправлена. Ответ сервера: {response.json()}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке цитаты: {e}")
        return False

if __name__ == "__main__":
    logger.info("Запуск бота для отправки мотивирующей цитаты")
    send_quote()
