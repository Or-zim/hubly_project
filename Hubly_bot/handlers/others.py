from aiogram import Router, F
from aiogram.types import Message
from Hubly_bot.keyboards.main_menu import get_start_mode_kb

router = Router()

@router.message(F.text == "🏠 В главное меню бота")
async def back_main_menu_command(message: Message):
    await message.answer(reply_markup=get_start_mode_kb())