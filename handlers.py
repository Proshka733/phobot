# ==========================================
# ЛОГИКА БОТА — УПРОЩЁННАЯ ВЕРСИЯ
# ==========================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import (
    ADMIN_ID, CHEF_ID, CAFE_NAME,
    DELIVERY_PRICE, DELIVERY_AREAS, WORK_HOURS
)
from menu import MENU
from keyboards import (
    main_menu, dishes_menu, dish_card,
    cart_menu, cancel_menu
)
from cart import (
    add_to_cart, clear_cart, get_cart_text,
    get_cart_text_for_admin, get_cart_text_for_chef, get_cart
)

router = Router()


class OrderForm(StatesGroup):
    address = State()
    phone = State()
    name = State()


# ---------- /start ----------
@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        f"🇻🇳 <b>{CAFE_NAME}</b>\n\n"
        f"Смачна в'єтнамська кухня з доставкою 🛵\n"
        f"Працюємо: {WORK_HOURS}\n"
        f"Доставка: {DELIVERY_AREAS}\n\n"
        f"Оберіть дію нижче 👇"
    )
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")


# ---------- КНОПКА "МЕНЮ" ----------
@router.message(F.text.contains("Меню"))
async def show_menu(message: Message):
    await message.answer(
        "🍜 <b>Наше меню</b>\n\nОберіть страву:",
        reply_markup=dishes_menu(),
        parse_mode="HTML"
    )


# ---------- КНОПКА "МІЙ КОШИК" ----------
@router.message(F.text.contains("кошик"))
async def show_cart(message: Message):
    text = get_cart_text(message.from_user.id)
    await message.answer(text, reply_markup=cart_menu(), parse_mode="HTML")


# ---------- КНОПКА "ДОСТАВКА" ----------
@router.message(F.text.contains("Доставка"))
async def show_delivery(message: Message):
    text = (
        "🚚 <b>Доставка</b>\n\n"
        f"Доставляємо у райони: <b>{DELIVERY_AREAS}</b>\n"
        f"Вартість доставки: <b>{DELIVERY_PRICE} грн</b>\n\n"
        "Готуємо свіжо після підтвердження замовлення.\n"
        "Оплата при отриманні — готівкою або карткою."
    )
    await message.answer(text, parse_mode="HTML")


# ---------- КНОПКА "ЗВ'ЯЗАТИСЯ З НАМИ" ----------
@router.message(F.text.contains("Зв'язатися"))
async def show_contacts(message: Message):
    text = (
        "📞 <b>Зв'язатися з нами</b>\n\n"
        "Якщо є питання щодо замовлення — напишіть нам.\n"
        "Ми відповімо найближчим часом."
    )
    await message.answer(text, parse_mode="HTML")


# ---------- НАЖАТИЕ НА БЛЮДО (d1, d2, ...) ----------
@router.callback_query(F.data.startswith("d"))
async def show_dish(callback: CallbackQuery):
    try:
        dish_id = int(callback.data[1:])
    except ValueError:
        await callback.answer("Помилка")
        return

    dish = next((d for d in MENU if d["id"] == dish_id), None)
    if not dish:
        await callback.answer("Страву не знайдено")
        return

    text = (
        f"<b>{dish['name']}</b>\n\n"
        f"{dish['desc']}\n\n"
        f"Порція: 750–800 г\n"
        f"Ціна: <b>{dish['price']} грн</b>"
    )

    if dish.get("photo"):
        await callback.message.answer_photo(
            photo=dish["photo"],
            caption=text,
            reply_markup=dish_card(dish_id),
            parse_mode="HTML"
        )
    else:
        await callback.message.answer(
            text,
            reply_markup=dish_card(dish_id),
            parse_mode="HTML"
        )

    await callback.answer()


# ---------- ДОБАВИТЬ В КОРЗИНУ (a1, a2, ...) ----------
@router.callback_query(F.data.startswith("a"))
async def add_dish(callback: CallbackQuery):
    try:
        dish_id = int(callback.data[1:])
    except ValueError:
        await callback.answer("Помилка")
        return

    add_to_cart(callback.from_user.id, dish_id)
    await callback.answer("✅ Додано до кошика!")


# ---------- НАЗАД В МЕНЮ (bm) ----------
@router.callback_query(F.data == "bm")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.answer(
        "🍜 <b>Наше меню</b>\n\nОберіть страву:",
        reply_markup=dishes_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


# ---------- ОЧИСТИТЬ КОРЗИНУ (cl) ----------
@router.callback_query(F.data == "cl")
async def clear(callback: CallbackQuery):
    clear_cart(callback.from_user.id)
    await callback.message.answer("🗑 Кошик очищено.")
    await callback.answer()


# ---------- ОФОРМИТИ ЗАМОВЛЕННЯ (ok) ----------
@router.callback_query(F.data == "ok")
async def checkout(callback: CallbackQuery, state: FSMContext):
    cart = get_cart(callback.from_user.id)
    if not cart:
        await callback.answer("Кошик порожній!", show_alert=True)
        return

    await callback.message.answer(
        "📍 Введіть адресу доставки:",
        reply_markup=cancel_menu()
    )
    await state.set_state(OrderForm.address)
    await callback.answer()


# ---------- ОТМЕНА (cx) ----------
@router.callback_query(F.data == "cx")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("❌ Оформлення скасовано.")
    await callback.answer()


# ---------- ШАГ 1: АДРЕС ----------
@router.message(OrderForm.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("📞 Введіть номер телефону:")
    await state.set_state(OrderForm.phone)


# ---------- ШАГ 2: ТЕЛЕФОН ----------
@router.message(OrderForm.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("👤 Введіть ваше ім'я:")
    await state.set_state(OrderForm.name)


# ---------- ШАГ 3: ИМЯ + ОТПРАВКА ----------
@router.message(OrderForm.name)
async def get_name(message: Message, state: FSMContext):
    data = await state.get_data()
    address = data.get("address")
    phone = data.get("phone")
    name = message.text
    user_id = message.from_user.id

    admin_text = get_cart_text_for_admin(user_id, name, address, phone)
    chef_text = get_cart_text_for_chef(user_id)

    try:
        await message.bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
    except Exception as e:
        print(f"Помилка відправки адміну: {e}")

    try:
        await message.bot.send_message(CHEF_ID, chef_text, parse_mode="HTML")
    except Exception as e:
        print(f"Помилка відправки кухарю: {e}")

    await message.answer(
        "✅ <b>Дякуємо! Ваше замовлення прийнято.</b>\n\n"
        "Ми зв'яжемося з вами найближчим часом для підтвердження.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

    clear_cart(user_id)
    await state.clear()


# ==========================================
# ЛОВЕЦ FILE_ID — ТОЛЬКО ДЛЯ АДМИНА
# Отправьте фото боту — он пришлёт file_id
# ==========================================

@router.message(F.photo)
async def catch_photo(message: Message):
    # Проверяем, что пишет админ
    if message.from_user.id != ADMIN_ID:
        await message.answer("Ця функція лише для адміна.")
        return

    # Берём последнее (самое качественное) фото
    photo = message.photo[-1]
    file_id = photo.file_id
    caption = message.caption or "без підпису"

    await message.answer(
        f"📸 <b>{caption}</b>\n\n"
        f"<code>{file_id}</code>\n\n"
        f"Скопіюйте цей код і вставте у menu.py",
        parse_mode="HTML"
    )
