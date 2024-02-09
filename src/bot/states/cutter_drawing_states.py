from aiogram.dispatcher.filters.state import State, StatesGroup


class CutterDrawingState(StatesGroup):
    cut_draw_option = State()
    cut_draw_data = State()
