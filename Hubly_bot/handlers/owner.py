from aiogram import Router, F, types
from aiogram.types import Message
from users.models import User
from Hubly_bot.keyboards.business import get_owner_profile_kb
from asgiref.sync import sync_to_async
from businesses.models import Business
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
router = Router()

@router.message(F.text == "👑 ВЛАДЕЛЕЦ")
async def business_role_owner_entry(message: Message):
    text = 'Вы выбрали роль владельца.\nВы можете ознакомится со своим бизнесом, посмотреть уведомления или обратится за помощью!'
    await message.answer(text=text, reply_markup=get_owner_profile_kb())

@router.message(F.text == '📂 Мои бизнесы')
async def show_user_businesses(message: Message, user: User):
    businesses = await sync_to_async(list)(user.owned_businesses.filter(is_active=True))
    if not businesses:
        await message.answer("У вас пока нет зарегистрированных бизнесов.\n"
            "Создайте первый через веб‑панель."
        )
        return

    text_kb = []
    for b in businesses:
        text_kb.append(InlineKeyboardButton(text=f'💰 {b}', callback_data=f"owner_business:{b.id}"))

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
           text_kb
        ]
    )

    await message.answer('Ваши бизнесы: ', reply_markup=kb)

