# ==========================================
# КНОПКИ БОТА — УПРОЩЁННАЯ ВЕРСИЯ
# ==========================================

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from menu import MENU


# ---------- ГЛАВНОЕ МЕНЮ (внизу экрана) ----------
def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍜 Меню")],
            [KeyboardButton(text="🛒 Мій кошик")],
            [KeyboardButton(text="🚚 Доставка")],
            [KeyboardButton(text="📞 Зв'язатися з нами")],
        ],
        resize_keyboard=True
    )
    return kb


# ---------- СПИСОК БЛЮД ----------
def dishes_menu():
    buttons = []
    for dish in MENU:
        buttons.append([
            InlineKeyboardButton(
                text=dish["name"],
                callback_data=f"d{dish['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ---------- КАРТОЧКА БЛЮДА ----------
def dish_card(dish_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Додати до замовлення",
                callback_data=f"a{dish_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад до меню",
                callback_data="bm"
            )
        ]
    ])


# ---------- КОРЗИНА ----------
def cart_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🟢 Оформити замовлення",
                callback_data="ok"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑 Очистити кошик",
                callback_data="cl"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад до меню",
                callback_data="bm"
            )
        ]
    ])


# ---------- ОТМЕНА ОФОРМЛЕНИЯ ----------
def cancel_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ Скасувати",
                callback_data="cx"
            )
        ]
    ])