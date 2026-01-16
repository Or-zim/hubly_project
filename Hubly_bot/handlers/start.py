from aiogram import Router, F, types
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message
from asgiref.sync import sync_to_async
from users.models import User, AuthToken
from businesses.models import Business
from clients.models import ClientRelation
from django.conf import settings 
from Hubly_bot.keyboards.main_menu import get_start_mode_kb
from Hubly_bot.keyboards.client import get_client_start_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, user: User):
    """хендлер для команды start"""

    payload = command.args

    if not payload:
        await message.answer(
            f"👋 Привет, {user.first_name}!\n\n"
            f"Добро пожаловать в <b>Hubly</b>.\n"
            f"Пожалуйста, выберите, как вы хотите использовать бота:",
            reply_markup=get_start_mode_kb()
        )
        return

    if payload.startswith("invite_"):
        await message.answer("🔑 Вы ввели код приглашения сотрудника (Функция в разработке)")
        return

    try:
        business = await Business.objects.aget(id=payload)
    except Business.DoesNotExist:
        await message.answer("❌ Ссылка недействительна. Компания не найдена.")
        return
    
    await sync_to_async(ClientRelation.objects.get_or_create)(user=user, business=business)
    
    text = (
            f"👋 Добро пожаловать в <b>«{business.name}»</b>!\n\n"
            f"Здесь вы можете записаться на услуги или посмотреть товары."
        )
    
    await message.answer(text=text, reply_markup=get_client_start_kb())


@router.message(Command("web"))
@router.message(F.text == "🌐 Открыть веб‑панель")
async def get_magic_link(message: types.Message, user: User):
    """
    Генерирует одноразовую ссылку для входа в веб-панель.
    """
    token_obj = await AuthToken.objects.acreate(user=user)

    domain = "http://127.0.0.1:8000" 
    link = f"{domain}/login/{token_obj.id}/"
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🚀 Перейти в CRM", url=link)]
    ])
    
    await message.answer(
        f"🔑 <b>Доступ к панели управления</b>\n\n"
        f"Нажмите кнопку ниже, чтобы войти в систему без пароля.\n"
        f"⏳ <i>Ссылка действует 2 минуты.</i>",
        reply_markup=keyboard
    )