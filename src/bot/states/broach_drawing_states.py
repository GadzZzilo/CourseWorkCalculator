from aiogram.dispatcher.filters.state import State, StatesGroup


class BroachDrawingState(StatesGroup):
    broach_draw_option = State()
    broach_draw_data = State()
