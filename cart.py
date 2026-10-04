# ==========================================
# КОРЗИНА — ХРАНЕНИЕ ЗАКАЗОВ ПОЛЬЗОВАТЕЛЕЙ
# ==========================================

from menu import MENU, MENU_VN
from config import DISH_PRICE, DELIVERY_PRICE


# Словарь: user_id -> {dish_id: quantity}
# Живёт в памяти, пока работает бот
carts = {}


def get_cart(user_id):
    """Получить корзину пользователя (создать, если нет)."""
    if user_id not in carts:
        carts[user_id] = {}
    return carts[user_id]


def add_to_cart(user_id, dish_id):
    """Добавить блюдо в корзину (+1)."""
    cart = get_cart(user_id)
    cart[dish_id] = cart.get(dish_id, 0) + 1


def remove_from_cart(user_id, dish_id):
    """Убрать блюдо из корзины (если было)."""
    cart = get_cart(user_id)
    if dish_id in cart:
        del cart[dish_id]


def clear_cart(user_id):
    """Очистить корзину полностью."""
    carts[user_id] = {}


def get_cart_text(user_id):
    """Текст корзины для клиента (украинский)."""
    cart = get_cart(user_id)

    if not cart:
        return "🛒 Ваш кошик порожній.\n\nОберіть страви у меню 🍜"

    lines = ["🛒 <b>Ваше замовлення:</b>\n"]
    total = 0

    for dish_id, qty in cart.items():
        dish = next((d for d in MENU if d["id"] == dish_id), None)
        if not dish:
            continue
        summa = dish["price"] * qty
        total += summa
        lines.append(f"{dish['name']} × {qty} — {summa} грн")

    lines.append("")
    lines.append(f"Сума: <b>{total} грн</b>")
    lines.append(f"Доставка: <b>{DELIVERY_PRICE} грн</b>")
    lines.append(f"<b>Разом: {total + DELIVERY_PRICE} грн</b>")

    return "\n".join(lines)


def get_cart_text_for_admin(user_id, client_name, address, phone):
    """Текст заказа для Ксении (украинский)."""
    cart = get_cart(user_id)
    lines = ["🔔 <b>НОВЕ ЗАМОВЛЕННЯ</b>\n"]
    total = 0

    for dish_id, qty in cart.items():
        dish = next((d for d in MENU if d["id"] == dish_id), None)
        if not dish:
            continue
        summa = dish["price"] * qty
        total += summa
        lines.append(f"{dish['name']} × {qty} — {summa} грн")

    lines.append("")
    lines.append(f"Сума: {total} грн")
    lines.append(f"Доставка: {DELIVERY_PRICE} грн")
    lines.append(f"<b>Разом: {total + DELIVERY_PRICE} грн</b>")
    lines.append("")
    lines.append(f"👤 Клієнт: {client_name}")
    lines.append(f"📍 Адреса: {address}")
    lines.append(f"📞 Телефон: {phone}")

    return "\n".join(lines)


def get_cart_text_for_chef(user_id):
    """Текст заказа для повара (вьетнамский)."""
    cart = get_cart(user_id)
    lines = ["🍜 <b>ĐƠN HÀNG MỚI</b>\n"]

    for dish_id, qty in cart.items():
        vn_name = MENU_VN.get(dish_id, f"Món {dish_id}")
        lines.append(f"{vn_name} × {qty}")

    lines.append("")
    lines.append(f"Tổng: {sum(d['price'] * q for d_id, q in cart.items() for d in MENU if d['id'] == d_id)} grn")

    return "\n".join(lines)