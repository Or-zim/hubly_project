from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from users.models import AuthToken


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
    