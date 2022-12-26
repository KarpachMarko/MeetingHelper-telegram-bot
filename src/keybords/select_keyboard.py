from typing import Dict, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class SelectKeyboard:

    _max_columns: int = 3

    _key_value_pairs: Dict[str, Dict[str, str]]
    _callback: CallbackData

    def __init__(self, key_value_pairs: Dict[str, Dict[str, str]], callback: CallbackData):
        self._key_value_pairs = key_value_pairs
        self._callback = callback

    @property
    def max_columns(self) -> int:
        return self._max_columns

    @max_columns.setter
    def max_columns(self, value):
        self._max_columns = value

    @property
    def key_value_pairs(self) -> Dict[str, Dict[str, str]]:
        return self._key_value_pairs

    @property
    def callback_id(self) -> str:
        return self._callback.prefix

    def generate_markup(self) -> InlineKeyboardMarkup:
        btn_rows: List[List[InlineKeyboardButton]] = []

        i = 0
        for key, value in self.key_value_pairs.items():
            button = InlineKeyboardButton(text=key, callback_data=self._callback.new(**value))
            row_index = i // self.max_columns

            if len(btn_rows) <= row_index:
                btn_rows.append([])
            btn_rows[row_index].append(button)

            i += 1

        return InlineKeyboardMarkup(inline_keyboard=btn_rows)
