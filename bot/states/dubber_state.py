from aiogram.fsm.state import State, StatesGroup

class DubberState(StatesGroup):
    choosing_title = State()
    choosing_episode = State()
    reporting_status = State()
    adding_comment = State()
    force_majeure = State()