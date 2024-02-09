from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)

from bot.services.payment import get_quickpay_form

from bot.services.payment import get_price


def get_kb(*args) -> ReplyKeyboardMarkup:
    """Creates a keyboard with buttons in a column"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    for button_name in args:
        kb.add(button_name)

    return kb


def get_pay_ikb(callback_data: list, label: str, service_type: str) -> InlineKeyboardMarkup:
    """Creates inline keyboard with buttons in a column"""
    ikb = InlineKeyboardMarkup(row_width=1)

    ib1 = InlineKeyboardButton("✅ Рассчитать",
                               callback_data=callback_data[0],
                               )
    ib2 = InlineKeyboardButton("❌ Отменить расчет", callback_data=callback_data[1])
    ib3 = InlineKeyboardButton(f"💵 Оплатить {get_price(price_type=service_type)} руб",
                               url=get_quickpay_form(label, service_type).redirected_url
                               )

    ikb.add(ib1).add(ib2).add(ib3)
    return ikb


def get_draw_ikb(options: list) -> InlineKeyboardMarkup:
    """Creates inline keyboard with buttons in a columns"""
    ikb = InlineKeyboardMarkup(row_width=5)

    for option in options:
        ib = InlineKeyboardButton(option, callback_data=option)
        ikb.insert(ib)

    ikb.add(InlineKeyboardButton("Отменить", callback_data="draw_cancel"))

    return ikb
