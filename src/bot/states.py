from aiogram.dispatcher.filters.state import StatesGroup, State


class BotStates(StatesGroup):
    invite_state = State()