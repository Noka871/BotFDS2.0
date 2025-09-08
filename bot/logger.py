import logging
import os
from datetime import datetime
from typing import Optional


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Настройка логгера с записью в файл и выводом в консоль
    """
    # Создаем папку для логов если ее нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Название файла лога с датой
    log_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"bot_{log_date}.log")

    # Создаем логгер
    logger = logging.getLogger(name or "bot")
    logger.setLevel(logging.DEBUG)

    # Проверяем, нет ли уже обработчиков у логгера
    if logger.handlers:
        return logger

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для файла
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Глобальный логгер
logger = setup_logger()


def log_command(user_id: int, username: str, command: str):
    """Логирование команд пользователя"""
    logger.info(f"User {user_id} ({username}) executed command: {command}")


def log_error(error_msg: str, exc_info=None):
    """Логирование ошибок"""
    logger.error(error_msg, exc_info=exc_info)


def log_database_operation(operation: str, details: str):
    """Логирование операций с БД"""
    logger.debug(f"DB Operation: {operation} - {details}")


def log_state_change(user_id: int, state_from: str, state_to: str):
    """Логирование изменения состояний FSM"""
    logger.debug(f"User {user_id} state changed: {state_from} -> {state_to}")