from django.contrib.auth import get_user_model


User = get_user_model()




async def async_create_user(
        telegram_id,
        first_name, 
        last_name,
        username, 
):
    safe_username = username if username else f"user_{telegram_id}"

    user, _ = await User.objects.aupdate_or_create(
        telegram_id=telegram_id,
        defaults={
            'first_name': first_name or '',
            'last_name': last_name or '',
            'username': safe_username
        }
    ) 
    return user



def sync_create_user(
        telegram_id,
        first_name, 
        last_name,
        username, 
):
    
    safe_username = username if username else f"user_{telegram_id}"
    user, _ = User.objects.update_or_create(
        telegram_id = telegram_id, 
        defaults={
            'first_name': first_name or '',
            'last_name': last_name or '',
            'username': safe_username
        }
    )

    return user