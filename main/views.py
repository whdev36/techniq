from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PlayerCreationForm
from .models import Player

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.first_name == '':
                messages.success(request, f'Xush kelibsiz {user.first_name}!')
            else:
                messages.success(request, f'Xush kelibsiz {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Hisob mavjud emas, tizimga kiring.')
    return render(request, 'main/home.html', {})


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'Siz tizimdan muvaffaqiyatli chiqdingiz.')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = PlayerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Roʻyxatdan oʻtish muvaffaqiyatli! Saytga xush kelibsiz.')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Roʻyxatdan oʻtishda xatolik yuz berdi. Quyidagi xatolarni tuzating.')
    else:
        form = PlayerCreationForm()
    return render(request, 'main/register.html', {'form': form})