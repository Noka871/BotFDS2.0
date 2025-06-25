from aiogram.fsm.state import StatesGroup, State

class ReportStates(StatesGroup):
    select_title = State()
    select_episode = State()
    report_status = State()
    delay_reason = State()