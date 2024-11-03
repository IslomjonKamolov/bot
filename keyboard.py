from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Form to'ldirish"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="@Artifex_Gravis",
)

user_access = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha"),
            KeyboardButton(text="Yo'q"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="@Artifex_Gravis",
)

contact_send_btn = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="kontaktni jo'natish", request_contact=True)],
    ],
)

channel_list = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ArGraV", url="https://t.me/Artifex_Gravis"),
        ],
        [
            InlineKeyboardButton(
                text="ArGraV portfolio", url="https://t.me/ArGraV_portfolio"
            )
        ],
    ],
)
