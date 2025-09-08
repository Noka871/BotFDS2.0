from aiogram.fsm.state import State, StatesGroup

class TimerState(StatesGroup):
    creating_title = State()
    creating_episodes = State()
    adding_dubbers = State()
    creating_broadcast = State()
    editing_title = State()