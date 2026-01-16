from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_client_start_kb(business_id):
    """меню клиента в конкретном бизнесе"""
    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="📅 Записаться / Услуги", callback_data=f"booking_{business_id}")],
            [InlineKeyboardButton(text="🛒 Товары", callback_data=f"shop_{business_id}"), InlineKeyboardButton(text="ℹ️ О нас", callback_data=f"about_{business_id}")],
            [InlineKeyboardButton(text="🏠 В главное меню бота", callback_data="back_to_main")]
        ]
    )
    return kb