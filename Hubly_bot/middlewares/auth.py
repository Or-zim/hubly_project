from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from users.models import User
from users.services import async_create_user

class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
            ) -> Any:
        
        tg_user = event.from_user
        if not tg_user:
            return await handler(event, data)
        
        user = await async_create_user(
            telegram_id=tg_user.id, 
            first_name = tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username
        )



        if user.is_blocked:
            if isinstance(event, Message):
                await event.answer("⛔ <b>Ваш аккаунт заблокирован администрацией.</b>")
            elif isinstance(event, CallbackQuery):
                await event.answer("⛔ Вы заблокированы.", show_alert=True)

            return
        

        data["user"] = user 
        return await handler(event, data)