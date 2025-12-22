from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from users.models import AuthToken
from businesses.models import Business
from .forms import BusinessCreationForm
from django.contrib import messages



def magic_login(request, token):

    auth_token = get_object_or_404(AuthToken, id=token)

    if not auth_token.is_valid():
        return render(request, 'web/error.html', {'message': 'Ссылка устарела ⌛'})
    
    login(request, auth_token.user)

    auth_token.delete()

    return redirect('web:dashboard')

@login_required
def dashboard(request):
    businesses = Business.objects.filter(owner=request.user, is_active=True)

    context = {
        'businesses': businesses,
    }
    return render(request, 'web/dashboard.html', context)



@login_required
def create_business_view(request):
    if request.method =='POST':
        form = BusinessCreationForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            messages.success(request, "Бизнес успешно создан 🎉")
            return redirect('web:dashboard')
    else:
        form = BusinessCreationForm()
    
    return render(request, 'web/create_business.html', {'form': form})