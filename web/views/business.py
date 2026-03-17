from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from businesses.models import Business, Module
from django.contrib import messages


@login_required
def create_business_wizard(request):
    """This func creates a new business"""
    if request.method == 'POST':
        name = request.POST.get('name')
        niche = request.POST.get('niche')
        selected_modules = request.POST.getlist('modules')
        business = Business.objects.create(owner=request.user, name=name, niche=niche)
        modules = Module.objects.filter(slug__in=selected_modules)
        business.enabled_modules.set(modules)
        messages.success(request, f"Бизнес «{name}» успешно создан и настроен! 🚀")
        return redirect('web:create_business')
    
    all_modules = Module.objects.all()
    return render(request, 'web/create_business_wizard.html', {
        'all_modules': all_modules,
        'niches': Business.NICHES
    })

@login_required
def business_main_view(request, bus_id):
    """This func shows your business"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    enabled_modules = business.enabled_modules.values_list('slug', flat=True)

    return render(request, 'web/workspace/dashboard.html', {
        'business': business,
        'enabled_modules': enabled_modules
    })

@login_required
def delete_business(request, bus_id):
    """This func deletes the selected business"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    business.orders.all().delete()
    business.delete()
    messages.success(request, "Бизнес успешно удален!")

    return redirect('web:index')
