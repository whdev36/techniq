from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PlayerCreationForm
from django.contrib.auth.hashers import check_password
from .models import Player

def home(request):
    template = loader.get_template('main/home.html')
    return HttpResponse(template.render({'page': 'home'}, request))

# 🔑 Optimize login and logout processes
def login_user(request):
    '''🔑 Login function so that the user can access the page'''
    if request.method == 'POST':
        username = request.POST.get('username')  # Use .get()
        password = request.POST.get('password')  # Use .get()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            welcome_message = f'Welcome {user.first_name or user.username}'
            messages.success(request, welcome_message)
            next_URL = request.GET.get('next', 'home')
            return redirect(next_URL)
        else:
            messages.warning(request, 'Invalid username or password. Please try again.')
    return render(request, 'auth/login.html', {})

@login_required
def logout_user(request):
    '''Log out the user and redirect to the home page.'''
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

def register_user(request):
    '''📝 Function for registration page'''
    if request.method == 'POST':
        form = PlayerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()    # Save the new user
            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful! Welcome to the site.')
            next_URL = request.GET.get('next', 'home')  # Redirect 'next' or 'home'
            return redirect(next_URL)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PlayerCreationForm()  # Render an empty form for GET request
    return render(request, 'auth/register.html', {'form': form})

@login_required
def delete_account(request):
    '''❌ User account deletion function'''
    if request.method == 'POST':
        player = get_object_or_404(Player, pk=request.user.pk)
        password = request.POST.get('confirm-password')  # Use .get()
        if not check_password(password, player.password):
            messages.error(request, 'Incorrect password. Please try again.')
            return redirect('delete-account')
        player.delete()
        logout(request)
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    return render(request, 'auth/delete-account.html', {})
