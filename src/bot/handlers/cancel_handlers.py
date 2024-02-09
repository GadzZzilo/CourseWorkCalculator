from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.keyboards.user_keyboard import get_kb


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply("Расчет отменен", reply_markup=get_kb(
        "Рассчитать резец",
        "Рассчитать протяжку",
        "Чертеж резца",
        "Чертеж протяжки"
    )
                        )


async def cancel_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await callback.message.reply("Расчет отменен", reply_markup=get_kb(
        "Рассчитать резец",
        "Рассчитать протяжку",
        "Чертеж резца",
        "Чертеж протяжки"
    )
                        )
    await callback.message.edit_reply_markup(reply_markup=None)


def register_cancel_handlers(dp: Dispatcher):
    dp.register_message_handler(
        cancel_handler,
        Text(equals="отменить", ignore_case=True),
        state="*"
    )
    dp.register_callback_query_handler(
        cancel_callback_handler,
        lambda callback: callback.data and callback.data == "draw_cancel",
        state="*"
    )