from aiogram import Dispatcher
from aiogram.utils import executor

from bot.bot_initialization import bot, dp
from bot.filters.middlewares import ThrottlingMiddleware
from bot.handlers.broach_fsm import register_broach_handlers
from bot.handlers.common_handlers import register_common_handlers
from bot.handlers.cutter_fsm import register_cutter_handlers
from bot.handlers.cutter_drawing import register_cutter_drawing_handlers
from bot.handlers.cancel_handlers import register_cancel_handlers
from bot.handlers.broach_drawing import register_broach_drawing_handlers


def register_handler(dp: Dispatcher) -> None:
    """Registers all handlers"""
    register_cancel_handlers(dp)
    register_cutter_handlers(dp)
    register_broach_handlers(dp)
    register_cutter_drawing_handlers(dp)
    register_broach_drawing_handlers(dp)
    register_common_handlers(dp)


register_handler(dp)

if __name__ == '__main__':
    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
