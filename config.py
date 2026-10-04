# ==========================================
# НАСТРОЙКИ — берутся из переменных окружения
# ==========================================

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "259428437"))
CHEF_ID = int(os.environ.get("CHEF_ID", "8975708586"))

CAFE_NAME = "В'єтнамська кухня"
DISH_PRICE = 200
DELIVERY_PRICE = 100
DELIVERY_AREAS = "Радужний та Шкільний"
WORK_HOURS = "11:00 – 22:00"