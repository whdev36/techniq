from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PlayerCreationForm
from .models import Player, Course, Lesson

def home(request):
    '''Handle user login and registration.'''

    courses = Course.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')  # Use .get to avoid KeyError
        password = request.POST.get('password')  # Use .get to avoid KeyError

        # Authenticated the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Use the user's first name if available, otherwise use the username
            welcome_message = f'Welcome {user.first_name or user.username}!'
            messages.success(request, welcome_message)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            # Handle invalid login credentials
            messages.error(request, 'Invalid username or password. Please try again.')
    # Render the home page for GET requests or failed login attempts
    return render(request, 'main/home.html', {'courses': courses})


@login_required
def logout_user(request):
    '''Log out the user and redirect to the home page.'''
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

def register_user(request):
    '''Handle user registration.'''
    if request.method == 'POST':
        form = PlayerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful! Welcome to the site.')
            next_url = request.GET.get('next', 'home')  # Redirect to 'next' or 'home'
            return redirect(next_url)
        else:
            # Display the form errors to the user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PlayerCreationForm()  # Render an empty form for GET requests
    return render(request, 'main/register.html', {'form': form})


def course_detail(request, course_id):
    '''Display details of a specific course, including its sections and lessons.'''
    course = get_object_or_404(Course, id=course_id)  # Fetch the course or return a 404 error
    sections = course.sections.all().order_by('order')  # Fetch sections ordered by their 'order' field
    return render(request, 'main/course_detail.html', {'course': course, 'sections': sections})

def lesson_detail(request, lesson_id):
    '''Display details of a specific lesson, including its content and quizzes.'''
    lesson = get_object_or_404(Lesson, id=lesson_id)  # Fetch the lesson or return a 404 error
    quizzes = lesson.quizzes.all()  # Fetch all quizzes for the lesson
    return render(request, 'main/lesson_detail.html', {'lesson': lesson, 'quizzes': quizzes})