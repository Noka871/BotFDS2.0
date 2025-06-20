# utils/states.py
class DubberStates(StatesGroup):
    select_title = State()
    select_episode = State()

class TimerStates(StatesGroup):
    create_title = State()