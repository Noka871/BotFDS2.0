"""
Модуль для управления уведомлениями
"""
import threading
import time
from datetime import datetime, timedelta
from telegram import Bot
from database import Database
from config import REMINDER_TIME_HOUR

class NotificationManager:
    def __init__(self, bot_token: str):
        """Инициализация менеджера уведомлений"""
        self.bot = Bot(token=bot_token)
        self.db = Database()
        self._stop_event = threading.Event()

    def start_daily_notifications(self):
        """Запуск фонового потока для ежедневных уведомлений"""
        thread = threading.Thread(target=self._daily_notification_loop)
        thread.daemon = True
        thread.start()

    def _daily_notification_loop(self):
        """Цикл ежедневных уведомлений"""
        while not self._stop_event.is_set():
            now = datetime.utcnow()
            target_time = now.replace(hour=REMINDER_TIME_HOUR, minute=0, second=0, microsecond=0)
            
            # Если текущее время уже прошло целевое, планируем на следующий день
            if now > target_time:
                target_time += timedelta(days=1)
            
            # Ожидание до целевого времени
            sleep_seconds = (target_time - now).total_seconds()
            time.sleep(sleep_seconds)
            
            # Отправка уведомлений
            self._send_pending_reminders()

    def _send_pending_reminders(self):
        """Отправка напоминаний о несданных сериях"""
        pending_episodes = self.db.get_pending_episodes()
        
        for episode in pending_episodes:
            message = self._format_reminder_message(episode)
            try:
                self.bot.send_message(chat_id=episode['dubber_id'], text=message)
            except Exception as e:
                print(f"Ошибка отправки уведомления пользователю {episode['dubber_id']}: {e}")

    def _format_reminder_message(self, episode: dict) -> str:
        """Форматирование сообщения-напоминания"""
        deadline = datetime.strptime(episode['deadline'], '%Y-%m-%d %H:%M:%S')
        is_overdue = datetime.now() > deadline
        
        status = "⚠️ Просрочено" if is_overdue else "⏳ Истекает скоро"
        deadline_str = deadline.strftime('%d.%m.%Y')
        
        return (
            f"🔔 Напоминание о серии!\n\n"
            f"Тайтл: {episode['title_name']}\n"
            f"Серия: {episode['episode_number']}\n"
            f"Срок сдачи: {deadline_str}\n"
            f"Статус: {status}\n\n"
            f"Пожалуйста, сдайте работу как можно скорее!"
        )

    def notify_new_marks(self, title_id: int):
        """Уведомление дабберов о готовности меток"""
        dubbers = self.db.get_title_dubbers(title_id)
        title_name = self.db.get_title_name(title_id)
        deadline = (datetime.now() + timedelta(days=2)).strftime('%d.%m.%Y')
        
        for dubber in dubbers:
            message = (
                f"🎧 Новые метки готовы!\n\n"
                f"Тайтл: {title_name}\n"
                f"Срок сдачи: {deadline}\n\n"
                f"У вас есть 2 дня на запись дорожки."
            )
            try:
                self.bot.send_message(chat_id=dubber['user_id'], text=message)
                # Установка дедлайна в БД
                self.db.set_episode_deadline(title_id, dubber['user_id'], datetime.now() + timedelta(days=2))
            except Exception as e:
                print(f"Ошибка уведомления даббера {dubber['user_id']}: {e}")

    def notify_penalty(self, dubber_id: int, amount: int, reason: str, title_name: str, episode_num: int):
        """Уведомление о назначении штрафа"""
        message = (
            f"🚨 Вам назначен штраф!\n\n"
            f"Тайтл: {title_name}\n"
            f"Серия: {episode_num}\n"
            f"Сумма: {amount} руб.\n"
            f"Причина: {reason}\n\n"
            f"По вопросам обращайтесь к таймеру."
        )
        self.bot.send_message(chat_id=dubber_id, text=message)

    def stop(self):
        """Остановка уведомлений"""
        self._stop_event.set()
        self.db.close()