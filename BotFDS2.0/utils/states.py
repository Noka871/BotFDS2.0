from aiogram.dispatcher.filters.state import StatesGroup, State

class ReportStates(StatesGroup):
    select_title = State()
    select_episode = State()
    confirm = State()