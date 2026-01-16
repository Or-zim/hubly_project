from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from pydantic import ValidationError
from users.models import AuthToken
from businesses.models import Business, Module
from .forms import BusinessCreationForm
from django.contrib import messages
from sales.services import process_order_sale




def magic_login(request, token):
    auth_token = get_object_or_404(AuthToken, id=token)
    if not auth_token.is_valid():
        return render(request, 'web/error.html', {'message': 'Ссылка устарела ⌛'})
    login(request, auth_token.user)
    auth_token.delete()
    return redirect('web:dashboard')

@login_required
def complete_sale(request, order_id):
    try:
        process_order_sale(order_id)
        messages.success(request, "Продажа успешно завершена! Склад обновлен.")
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect('web:order_detail', order_id=order_id)


@login_required
def create_business_wizard(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        niche = request.POST.get('niche')
        selected_modules = request.POST.getlist('modules')
        business = Business.objects.create(owner=request.user, name=name, niche=niche)
        modules = Module.objects.filter(slug__in=selected_modules)
        business.enabled_modules.set(modules)
        messages.success(request, f"Бизнес «{name}» успешно создан и настроен! 🚀")
        return redirect('web:dashboard')
    
    all_modules = Module.objects.all()
    return render(request, 'web/create_business_wizard.html', {
        'all_modules': all_modules,
        'niches': Business.NICHES
    })

def index_view(request):
    if request.user.is_authenticated:
        businesses = request.user.owned_businesses.all()
        return render(request, 'web/dashboard.html', {
            'businesses': businesses
        })
    else:
        return render(request, 'web/landing.html')