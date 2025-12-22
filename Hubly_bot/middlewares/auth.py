from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from users.models import User

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
        
        safe_username = tg_user.username if tg_user.username else f"user_{tg_user.id}"
        
        current_data = {
            'first_name': tg_user.first_name or '',
            'last_name': tg_user.last_name or '',
            'username': safe_username, 
        }


        user, created = await User.objects.aget_or_create(
            telegram_id=tg_user.id,
            defaults=current_data
        )

        if not created:
            has_changes = False
            
            if user.username != safe_username:
                user.username = safe_username
                has_changes = True
                
            if user.first_name != current_data['first_name']:
                user.first_name = current_data['first_name']
                has_changes = True
                
            if user.last_name != current_data['last_name']:
                user.last_name = current_data['last_name']
                has_changes = True
            
            if has_changes:
                await user.asave()  


        if user.is_blocked:
            if isinstance(event, Message):
                await event.answer("⛔ <b>Ваш аккаунт заблокирован администрацией.</b>")
            elif isinstance(event, CallbackQuery):
                await event.answer("⛔ Вы заблокированы.", show_alert=True)

            return
        

        data["user"] = user 
        return await handler(event, data)