from aiogram.dispatcher.filters.state import StatesGroup, State

class DubberStates(StatesGroup):
    select_title = State()
    report_status = State()

class TimerStates(StatesGroup):
    create_title = State()