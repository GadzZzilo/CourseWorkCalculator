import os

from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile

from bot.keyboards.user_keyboard import get_pay_ikb, get_kb
from bot.services.engine.main import start_calculate
from bot.services.payment import check_payment, get_label
from bot.states.broach_drawing_states import BroachDrawingState

from bot.keyboards.user_keyboard import get_draw_ikb

from bot.services.tables import broach_options


async def broach_drawing_option_command(message: types.Message):
    await BroachDrawingState.broach_draw_option.set()
    await message.answer(
        "Выберите вариант протяжки из представленных",
        reply_markup=get_draw_ikb(items=broach_options)
    )


async def broach_drawing_option_invalid_callback(callback: types.CallbackQuery):
    await callback.message.reply(
        "Я не знаю такого варианта протяжки. 🤷‍♀️ Выберите вариант протяжки из представленных",
        reply_markup=get_draw_ikb(
            items=broach_options)
    )


async def broach_drawing_not_paid_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback.message.answer(
            f"Чтобы бот смог приступить к расчету, сперва необходимо оплатить  💰",
            reply_markup=get_pay_ikb(
                [f"draw_broach success {'paid' if check_payment(data['label']) else 'not paid'}",
                 "draw_broach fail"
                 ],
                label=data["label"],
                service_type="draw"
            )
        )
    await callback.answer(
        "Чтобы бот смог приступить к расчету, сперва необходимо произвести оплату (нажмите кнопку 'оплатить')"
        "\nЕсли вы уже оплатили, нажмите 'Рассчитать' еще раз",
        show_alert=True
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()


async def broach_option_callback(callback: types.CallbackQuery, state: FSMContext):
    await BroachDrawingState.broach_draw_data.set()
    async with state.proxy() as data:
        if os.path.exists(f"bot/static/drawings_of_broaches/{callback.data}.cdw"):
            data["label"] = get_label()
            data["option"] = callback.data + ".cdw"
            await callback.message.answer(
                f"Чтобы бот смог приступить к расчету, сперва необходимо оплатить  💰",
                reply_markup=get_pay_ikb(
                    [f"draw_broach success {'paid' if check_payment(data['label']) else 'not paid'}",
                     "draw_broach fail"
                     ],
                    label=data["label"],
                    service_type="draw"
                )
            )
        else:
            await callback.message.answer(
                f"К сожалению, бот не может решить ваш вариант 😞. Вы можете написать нам, чтобы заказать чертеж:\nhttps://t.me/tonitaga\nhttps://t.me/KaaaSnake",
                disable_web_page_preview=True
            )
            await callback.message.edit_reply_markup(reply_markup=None)
            await state.finish()


async def broach_drawing_callback(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.data == "draw_broach success paid" and check_payment(data["label"]):
            await callback.answer("Приступил к расчетам. Ожидайте...", show_alert=True)

            file_name = f"bot/static/drawings_of_broaches/{data['option']}"

            with open(file_name, "rb") as file:
                await callback.message.reply_document(file)

            await callback.message.edit_reply_markup(reply_markup=None)
            await state.finish()
        else:
            await callback.answer("Расчет отменен ❌", show_alert=True)
        await callback.message.edit_reply_markup(reply_markup=None)
        await state.finish()


def register_broach_drawing_handlers(dp: Dispatcher):
    """Registers cutter handlers"""
    dp.register_message_handler(broach_drawing_option_command, Text(equals="Чертеж протяжки", ignore_case=True))

    dp.register_callback_query_handler(
        broach_drawing_option_invalid_callback,
        lambda callback: callback.data and callback.data not in broach_options,
        state=BroachDrawingState.broach_draw_option
    )
    dp.register_callback_query_handler(
        broach_option_callback,
        lambda callback: callback.data and callback.data in broach_options,
        state=BroachDrawingState.broach_draw_option
    )
    dp.register_callback_query_handler(
        broach_drawing_not_paid_callback,
        lambda callback: callback.data and "not paid" in callback.data,
        state=BroachDrawingState.broach_draw_data
    )

    dp.register_callback_query_handler(
        broach_drawing_callback,
        lambda callback: callback.data and callback.data.startswith("draw_broach"),
        state=BroachDrawingState.broach_draw_data
    )
