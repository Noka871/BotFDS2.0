"""
Обработчики для функционала даббера
"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.database import get_db
from services.dubber_service import DubberService
from keyboards.dubber_menu import get_dubber_menu, get_episode_status_keyboard
import logging
from typing import List


class DubberStates(StatesGroup):
    """Состояния FSM для workflow даббера"""
    selecting_title = State()  # Выбор тайтла
    selecting_episode = State()  # Выбор серии
    reporting_status = State()  # Выбор статуса сдачи
    reporting_delay = State()  # Указание причины задержки
    force_majeure = State()  # Сообщение о форс-мажоре


async def handle_select_title(message: types.Message, state: FSMContext):
    """
    Обработчик кнопки 'Выбрать тайтл'
    Показывает пользователю список его тайтлов
    """
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    logging.info(f"Нажата кнопка 'Выбрать тайтл' от {user_id} ({username})")

    try:
        # Получаем сессию базы данных
        db = next(get_db())
        service = DubberService(db)

        # Получаем тайтлы пользователя
        titles = service.get_user_titles(user_id)

        if not titles:
            await message.answer("📭 У вас нет назначенных тайтлов.")
            return

        # Сохраняем тайтлы в состоянии для последующего использования
        async with state.proxy() as data:
            data['user_titles'] = titles
            data['titles_dict'] = {i + 1: title for i, title in enumerate(titles)}

        # Формируем красивое сообщение со списком тайтлов
        response = "🎬 <b>Ваши тайтлы:</b>\n\n"
        for i, title in enumerate(titles, 1):
            response += (f"<b>{i}.</b> {title.name}\n"
                         f"   📺 Текущая серия: <b>{title.current_episode}/{title.total_episodes}</b>\n"
                         f"   🆔 ID: <code>{title.id}</code>\n\n")

        response += "Введите <b>номер</b> тайтла для отчета:"
        await message.answer(response, parse_mode='HTML')
        await DubberStates.selecting_title.set()

    except Exception as e:
        logging.error(f"Ошибка при получении тайтлов пользователя {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при получении ваших тайтлов. Попробуйте позже.")


async def handle_title_selection(message: types.Message, state: FSMContext):
    """
    Обработчик выбора тайтла из списка
    Переходит к выбору серии для отчета
    """
    user_id = message.from_user.id

    try:
        # Пытаемся преобразовать ввод в число
        title_index = int(message.text.strip())

        async with state.proxy() as data:
            titles_dict = data.get('titles_dict', {})

        # Проверяем корректность выбора
        if title_index not in titles_dict:
            await message.answer("❌ Неверный номер тайтла. Пожалуйста, выберите номер из списка:")
            return

        selected_title = titles_dict[title_index]

        # Сохраняем выбранный тайтл в состоянии
        async with state.proxy() as data:
            data['selected_title'] = selected_title
            data['selected_title_id'] = selected_title.id

        # Формируем информационное сообщение о выбранном тайтле
        response = (f"🎬 <b>Выбран тайтл:</b> {selected_title.name}\n"
                    f"📺 <b>Текущая серия:</b> {selected_title.current_episode}\n"
                    f"🔢 <b>Всего серий:</b> {selected_title.total_episodes}\n\n"
                    f"Введите <b>номер серии</b> для отчета (1-{selected_title.total_episodes}):")

        await message.answer(response, parse_mode='HTML')
        await DubberStates.selecting_episode.set()

    except ValueError:
        await message.answer("❌ Пожалуйста, введите <b>номер</b> тайтла (цифру):", parse_mode='HTML')
    except Exception as e:
        logging.error(f"Ошибка при выборе тайтла пользователем {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при обработке выбора. Попробуйте снова.")


async def handle_episode_selection(message: types.Message, state: FSMContext):
    """
    Обработчик выбора номера серии
    Переходит к выбору статуса сдачи
    """
    user_id = message.from_user.id

    try:
        # Парсим номер серии
        episode = int(message.text.strip())

        async with state.proxy() as data:
            selected_title = data.get('selected_title')

        if not selected_title:
            await message.answer("❌ Не удалось определить выбранный тайтл. Начните заново.")
            await state.finish()
            return

        # Проверяем корректность номера серии
        if episode < 1 or episode > selected_title.total_episodes:
            await message.answer(
                f"❌ Неверный номер серии. Допустимый диапазон: 1-{selected_title.total_episodes}\n"
                "Пожалуйста, введите корректный номер:"
            )
            return

        # Сохраняем выбранную серию в состоянии
        async with state.proxy() as data:
            data['selected_episode'] = episode

        # Предлагаем выбрать статус сдачи
        response = (f"📋 <b>Тайтл:</b> {selected_title.name}\n"
                    f"🎯 <b>Серия:</b> {episode}\n\n"
                    f"<b>Выберите статус сдачи:</b>")

        await message.answer(response, parse_mode='HTML', reply_markup=get_episode_status_keyboard())
        await DubberStates.reporting_status.set()

    except ValueError:
        await message.answer("❌ Пожалуйста, введите <b>номер серии</b> (цифру):", parse_mode='HTML')
    except Exception as e:
        logging.error(f"Ошибка при выборе серии пользователем {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при обработке выбора. Попробуйте снова.")


async def handle_status_selection(message: types.Message, state: FSMContext):
    """
    Обработчик выбора статуса сдачи
    Обрабатывает 'Серию сдал' или переходит к вводу причины задержки
    """
    user_id = message.from_user.id
    status_text = message.text

    # Проверяем валидность выбора
    if status_text not in ['Серию сдал', 'Серию задержу']:
        await message.answer("❌ Пожалуйста, выберите вариант из предложенных кнопок:")
        return

    if status_text == 'Серию сдал':
        # Немедленная обработка сдачи
        await handle_episode_submitted(message, state)
    else:
        # Переход к вводу причины задержки
        await message.answer("📝 Пожалуйста, укажите <b>причину задержки</b>:",
                             parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
        await DubberStates.reporting_delay.set()


async def handle_episode_submitted(message: types.Message, state: FSMContext):
    """
    Обработчик успешной сдачи серии
    Сохраняет отчет в базу данных
    """
    user_id = message.from_user.id

    try:
        async with state.proxy() as data:
            selected_title = data.get('selected_title')
            episode = data.get('selected_episode')

        if not selected_title or episode is None:
            await message.answer("❌ Ошибка данных. Начните процесс заново.")
            await state.finish()
            return

        # Получаем сессию базы данных
        db = next(get_db())
        service = DubberService(db)

        # Сохраняем отчет о сдаче
        report = service.create_report(
            user_id=user_id,
            title_id=selected_title.id,
            episode=episode,
            status='submitted'
        )

        # Формируем сообщение об успехе
        response = (f"✅ <b>Спасибо за предоставленную информацию!</b>\n\n"
                    f"🎬 <b>Тайтл:</b> {selected_title.name}\n"
                    f"🎯 <b>Серия:</b> {episode}\n"
                    f"🕒 <b>Время сдачи:</b> {report.submitted_at.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"Хотите добавить еще серию?")

        await message.answer(response, parse_mode='HTML', reply_markup=get_dubber_menu())
        await state.finish()

    except Exception as e:
        logging.error(f"Ошибка при сохранении отчета пользователя {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при сохранении отчета. Попробуйте позже.")
        await state.finish()


async def handle_delay_reason(message: types.Message, state: FSMContext):
    """
    Обработчик ввода причины задержки
    Сохраняет отчет о задержке в базу данных
    """
    user_id = message.from_user.id
    delay_reason = message.text

    try:
        async with state.proxy() as data:
            selected_title = data.get('selected_title')
            episode = data.get('selected_episode')

        if not selected_title or episode is None:
            await message.answer("❌ Ошибка данных. Начните процесс заново.")
            await state.finish()
            return

        # Получаем сессию базы данных
        db = next(get_db())
        service = DubberService(db)

        # Сохраняем отчет о задержке
        report = service.create_report(
            user_id=user_id,
            title_id=selected_title.id,
            episode=episode,
            status='delayed',
            comment=delay_reason
        )

        # Формируем сообщение об успехе
        response = (f"✅ <b>Спасибо за предоставленную информацию!</b>\n\n"
                    f"🎬 <b>Тайтл:</b> {selected_title.name}\n"
                    f"🎯 <b>Серия:</b> {episode}\n"
                    f"📝 <b>Причина задержки:</b> {delay_reason}\n\n"
                    f"Администрация будет уведомлена о вашей ситуации.\n"
                    f"Хотите добавить еще серию?")

        await message.answer(response, parse_mode='HTML', reply_markup=get_dubber_menu())
        await state.finish()

    except Exception as e:
        logging.error(f"Ошибка при сохранении задержки пользователя {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при сохранении информации о задержке. Попробуйте позже.")
        await state.finish()


async def handle_add_timer_role(message: types.Message):
    """
    Обработчик кнопки 'Добавить роль таймера'
    Изменяет роль пользователя на 'timer'
    """
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    logging.info(f"Нажата кнопка 'Добавить роль таймера' от {user_id} ({username})")

    try:
        # Получаем сессию базы данных
        db = next(get_db())
        service = DubberService(db)

        # Обновляем роль пользователя
        user = service.update_user_role(user_id, 'timer')

        if user:
            response = (f"✅ <b>Вам успешно выданы права таймера!</b>\n\n"
                        f"Теперь вы можете:\n"
                        f"• Создавать новые тайтлы\n"
                        f"• Редактировать существующие тайтлы\n"
                        f"• Просматривать график сдавших\n"
                        f"• Создавать рассылки\n\n"
                        f"Хотите добавить тайтл?")

            await message.answer(response, parse_mode='HTML')
        else:
            await message.answer("❌ Пользователь не найден.")

    except Exception as e:
        logging.error(f"Ошибка при добавлении роли таймера пользователю {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при добавлении роли. Попробуйте позже.")


async def handle_force_majeure(message: types.Message, state: FSMContext):
    """
    Обработчик кнопки 'Форс-мажор'
    Начинает процесс уведомления о форс-мажоре
    """
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    logging.info(f"Нажата кнопка 'Форс-мажор' от {user_id} ({username})")

    await message.answer(
        "⚠️ <b>Что произошло? О чем вы хотите предупредить?</b>\n\n"
        "Опишите ситуацию подробно, чтобы администрация могла понять "
        "и принять соответствующие меры:",
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await DubberStates.force_majeure.set()


async def handle_force_majeure_message(message: types.Message, state: FSMContext):
    """
    Обработчик сообщения о форс-мажоре
    Сохраняет уведомление в базу данных
    """
    user_id = message.from_user.id
    message_text = message.text

    try:
        # Получаем сессию базы данных
        db = next(get_db())
        service = DubberService(db)

        # Сохраняем сообщение о форс-мажоре
        force_majeure = service.create_force_majeure(user_id, message_text)

        response = (f"✅ <b>Ваше сообщение сохранено!</b>\n\n"
                    f"📝 <b>Текст:</b> {message_text}\n"
                    f"🕒 <b>Время отправки:</b> {force_majeure.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"Администрация будет уведомлена и рассмотрит вашу ситуацию.")

        await message.answer(response, parse_mode='HTML', reply_markup=get_dubber_menu())
        await state.finish()

    except Exception as e:
        logging.error(f"Ошибка при сохранении форс-мажора пользователя {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при сохранении сообщения. Попробуйте позже.")
        await state.finish()


async def handle_my_debts(message: types.Message):
    """
    Обработчик кнопки 'Мои долги'
    Показывает пользователю список несданных серий
    """
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    logging.info(f"Нажата кнопка 'Мои долги' от {user_id} ({username})")

    try:
        # Получаем сессию базы данных
        db = next(get_db())
        service = DubberService(db)

        # Получаем долги пользователя
        debts = service.get_user_debts(user_id)

        if not debts:
            await message.answer("✅ <b>У вас нет текущих долгов!</b>\n\nВсе серии сданы вовремя. 👍",
                                 parse_mode='HTML')
            return

        # Формируем подробный отчет о долгах
        response = "📋 <b>Ваши текущие долги:</b>\n\n"

        total_debts = 0
        delayed_debts = 0

        for debt in debts:
            total_debts += 1
            if debt['is_delayed']:
                delayed_debts += 1

            status_icon = "🔴" if debt['status'] == 'not_submitted' else "🟡"
            status_text = "Не сдано" if debt['status'] == 'not_submitted' else "Задержано"

            response += (f"{status_icon} <b>{debt['title_name']}</b> - Серия {debt['episode']}\n"
                         f"   📊 Статус: <b>{status_text}</b>\n")

            if debt['is_delayed'] and debt['comment']:
                response += f"   📝 Причина: {debt['comment']}\n"

            response += "\n"

        # Добавляем статистику
        response += (f"\n📈 <b>Статистика:</b>\n"
                     f"• Всего долгов: <b>{total_debts}</b>\n"
                     f"• Задержано: <b>{delayed_debts}</b>\n"
                     f"• Не сдано: <b>{total_debts - delayed_debts}</b>")

        await message.answer(response, parse_mode='HTML')

    except Exception as e:
        logging.error(f"Ошибка при получении долгов пользователя {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при получении информации о долгах. Попробуйте позже.")


def register_dubber_handlers(dp: Dispatcher):
    """
    Регистрация всех обработчиков для функционала даббера
    Args:
        dp: Dispatcher Aiogram
    """
    # Обработчики кнопок меню
    dp.register_message_handler(handle_select_title, lambda message: message.text == 'Выбрать тайтл', state=None)
    dp.register_message_handler(handle_add_timer_role, lambda message: message.text == 'Добавить роль таймера')
    dp.register_message_handler(handle_force_majeure, lambda message: message.text == 'Форс-мажор')
    dp.register_message_handler(handle_my_debts, lambda message: message.text == 'Мои долги')

    # Обработчики состояний FSM
    dp.register_message_handler(handle_title_selection, state=DubberStates.selecting_title)
    dp.register_message_handler(handle_episode_selection, state=DubberStates.selecting_episode)
    dp.register_message_handler(handle_status_selection, state=DubberStates.reporting_status)
    dp.register_message_handler(handle_delay_reason, state=DubberStates.reporting_delay)
    dp.register_message_handler(handle_force_majeure_message, state=DubberStates.force_majeure)