from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_start_mode_kb():
    """создание меню для выбора режима"""

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨‍💼 Режим Бизнеса"), KeyboardButton(text="👤 Режим Клиента")],
            [KeyboardButton(text="🆘 Поддержка"), KeyboardButton(text="ℹ️ О сервисе")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите режим работы..."
    )

    return kb

def get_choose_role_kb():
    """клавиатура выбора роли владельца или сотрудника"""

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👑 ВЛАДЕЛЕЦ")],
            [KeyboardButton(text="👷 СОТРУДНИК")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите роль..."
    )

    return kb