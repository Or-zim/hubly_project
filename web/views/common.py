from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from users.models import AuthToken
import hashlib
import hmac
import time
from django.conf import settings
from django.http import HttpResponseForbidden
from users.services import sync_create_user
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

def magic_login(request, token):
    """This func creates a new auth_token for loggin in to the system"""
    auth_token = get_object_or_404(AuthToken, id=token)
    if not auth_token.is_valid():
        return render(request, 'web/error.html', {'message': 'Ссылка устарела ⌛'})
    login(request, auth_token.user)
    auth_token.delete()
    return redirect('web:index')

def index_view(request):
    """This func shows the main window and the main page"""
    if request.user.is_authenticated:
        businesses = request.user.owned_businesses.all()
        return render(request, 'web/dashboard.html', {
            'businesses': businesses
        })
    else:
        return render(request, 'web/landing.html')
    
def verify_telegram_data(data, bot_token):
    
    received_hash = data.get('hast')
    if not received_hash:
        return False
    
    data_check_list = [f"{k}={v}" for k, v in sorted(data.items()) if k != 'hash']
    data_check_string = '\n'.join(data_check_list)

    secret_key = hashlib.sha256(bot_token.encode('utf-8')).digest()
    expected_hash = hmac.new(
        secret_key, 
        data_check_string.encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()

    if expected_hash == received_hash:
        auth_date = int(data.get('auth_date', 0))
        if time.time() - auth_date < 86400:
            return True
    return False

def telegram_login_widget_view(request):

    telegram_data = request.get('data')

    token = BOT_TOKEN

    if verify_telegram_data(telegram_data, token):

        user = sync_create_user(
            telegram_id=int(telegram_data.get('id')),
            first_name=telegram_data.get('first_name'),
            last_name=telegram_data.get('last_name'),
            username=telegram_data.get('username')
        )

        if user.is_blocked:
            return HttpResponseForbidden("⛔ Ваш аккаунт заблокирован администрацией.")

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        print(f"!!! DEBUG: Пользователь {request.user.username} авторизован: {request.user.is_authenticated}")
        print(f"!!! DEBUG: Ключ сессии: {request.session.session_key}")
    
        return redirect('web:index')
    
    return HttpResponseForbidden("Ошибка авторизации. Данные подделаны.")
        
def logout_user(request):
    logout(request)
    return redirect('web:index') 