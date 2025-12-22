from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_owner_profile_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📂 Мои бизнесы"), KeyboardButton(text="🔔 Уведомления")],
            [KeyboardButton(text="🌐 Открыть веб‑панель"), KeyboardButton(text="❓ Помощь / Обучение")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

    return kb