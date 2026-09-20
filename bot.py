import os
import logging
from flask import Flask
from threading import Thread

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# -----------------------------
# تنظیمات
# -----------------------------

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN تنظیم نشده است")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# -----------------------------
# منوی کافه رادسام
# -----------------------------

MENU = {
    "rad1": ("تک رادسام", 90000),
    "rad2": ("دبل رادسام", 100000),
    "mark1": ("تک مارک", 130000),
    "mark2": ("دبل مارک", 150000),
    "capp": ("کاپوچینو", 180000),
    "kark": ("چای کرک", 180000),
    "masala": ("چای ماسالا", 180000),
    "pistachio": ("کرک پسته", 200000),
    "hot": ("شکلات داغ", 180000),
}

# سبد خرید کاربران
carts = {}

# اطلاعات موقت سفارش
orders = {}


# -----------------------------
# ابزارها
# -----------------------------

def money(number):
    return f"{number:,}".replace(",", "٬") + " تومان"


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 منوی کافه", callback_data="menu")],
        [InlineKeyboardButton("🛒 سبد خرید", callback_data="cart")],
        [InlineKeyboardButton("📦 ثبت سفارش", callback_data="checkout")],
        [InlineKeyboardButton("📍 آدرس کافه", callback_data="address")],
        [InlineKeyboardButton("📞 تماس با ما", callback_data="contact")],
    ])


def menu_keyboard():
    buttons = []

    for key, (name, price) in MENU.items():
        buttons.append([
            InlineKeyboardButton(
                f"{name} — {money(price)}",
                callback
