from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from asgiref.sync import sync_to_async

from users.models import User
from businesses.models import Business, Staff
from clients.models import ClientRelation 
from Hubly_bot.keyboards.client import get_client_start_kb
from Hubly_bot.keyboards.main_menu import get_choose_role_kb

router = Router()

@router.message(F.text == "👨‍💼 Режим Бизнеса")
async def business_mode_entry(message: Message, user: User):
    await message.answer("Вы выбрали 👨‍💼 Режим Бизнеса!\nВыберите вашу роль: ", reply_markup=get_choose_role_kb())
    
@router.message(F.text == "👤 Режим Клиента")
async def clients_mode_entry(message: Message):
    await message.answer("Вы выбрали 👤 Режим Клиента!\n Вы можите воспользоваться дальнейшими услугами!", reply_markup=get_client_start_kb())

@router.message(F.text == "👷 СОТРУДНИК")
async def business_role_staff_enter(message: Message):
    await message.answer('Вы выбрали роль 👷 СОТРУДНИК!')

