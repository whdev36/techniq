from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
