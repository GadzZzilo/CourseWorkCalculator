from aiogram import Dispatcher, types
from aiogram.types import ContentType

from bot.keyboards.user_keyboard import get_kb


async def start_command(message: types.Message):
    await message.answer(
        f"Привет тебе, {message.from_user.first_name}!\nИспользуй /help, чтобы увидеть возможности бота 🦾",
        reply_markup=get_kb("Рассчитать резец", "Рассчитать протяжку", "Чертеж резца", "Чертеж протяжки",  "/preview")
    )


async def support_command(message: types.Message):
    await message.answer(
        f"Если у вас есть вопросы или предложения пишите нам:\nhttps://t.me/tonitaga\nhttps://t.me/KaaaSnake",
        disable_web_page_preview=True,
        reply_markup=get_kb("Рассчитать резец", "Рассчитать протяжку", "Чертеж резца", "Чертеж протяжки", "/preview")
    )


async def example_command(message: types.Message):
    with open("bot/static/broach_preview.png", "rb") as photo_broach,\
        open("bot/static/circle_preview.png", "rb") as photo_circle, \
            open("bot/static/prismatic_preview.png", "rb") as photo_prismatic:

        media = types.MediaGroup()

        media.attach_photo(types.InputFile(photo_circle), "Пример расчета круглого резца")
        media.attach_photo(types.InputFile(photo_prismatic), "Пример расчета призматического резца")
        media.attach_photo(types.InputFile(photo_broach), "Пример расчета протяжки")

        await message.reply_media_group(media=media)


async def help_command(message: types.Message):
    msg = """
Этот бот рассчитывает все значения для резца и протяжки курсовой 'Формообразующий инструмент' Иевлева 😎
<b>/start</b> - <em> начало работы с ботом </em>
<b>/help</b> - <em>информация о командах</em>
<b>/support</b> - <em>связь с разработчиками</em>
<b>/preview</b> - <em>показывает пример расчета</em>
<b>Рассчитать резец</b> - <em>для расчета резца</em>
<b>Рассчитать протяжку</b> - <em>для расчета протяжки</em>
<b>Чертеж резца</b> - <em>для покупки компас-файла резца</em>
<b>Чертеж протяжки</b> - <em>для покупки компас-файла протяжки</em>
"""
    await message.answer(msg, parse_mode="HTML")


async def unknown_command(message: types.Message) -> None:
    """Processes all types of messages"""
    await message.answer(
        "Я не знаю, что вы от меня хотите 🤔\n"
        "Просто напомню, что есть комманда /help",
        reply_markup=get_kb("Рассчитать резец", "Рассчитать протяжку", "Чертеж резца", "Чертеж протяжки")
    )


def register_common_handlers(dp: Dispatcher):
    """Registers common handlers"""
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(support_command, commands=["support"])
    dp.register_message_handler(example_command, commands=["preview"])
    dp.register_message_handler(help_command, commands=["help"])
    dp.register_message_handler(unknown_command, content_types=ContentType.ANY)
