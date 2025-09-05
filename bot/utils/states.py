from aiogram.fsm.state import State, StatesGroup

class DubberStates(StatesGroup):
    selecting_title = State()
    selecting_episode = State()
    reporting_status = State()
    adding_comment = State()

class TimerStates(StatesGroup):
    creating_title = State()
    waiting_for_title_name = State()
    waiting_for_episodes_count = State()
    waiting_for_dubbers = State()
    editing_title = State()
    selecting_title_to_edit = State()
    broadcasting = State()
    selecting_title_for_broadcast = State()
    waiting_for_broadcast_message = State()

class AdminStates(StatesGroup):
    generating_report = State()
    sending_notification = State()