# Состояния FSM
from aiogram.fsm.state import State, StatesGroup

class DubbingStates(StatesGroup):
    """Состояния для работы с дабберами"""
    select_title = State()
    select_episode = State()
    report_status = State()
    add_comment = State()

class TimerStates(StatesGroup):
    """Состояния для работы с таймерами"""
    create_title = State()
    edit_title = State()
    send_notification = State()