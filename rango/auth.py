from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserPasswordChangeForm
from .models import UserProfile


# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # Create a corresponding UserProfile
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('rango:login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    print(form.errors)
    return render(request, 'registration/register.html', {'form': form})

# User login view
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, 'Login successful.')
                    return redirect('rango:index')
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid login form.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})

# Modify the password view
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to stay signed in
            messages.success(request, 'Your password was successfully updated.')
            return redirect('rango:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserPasswordChangeForm(request.user)

    print(form)
    return render(request, 'registration/change_password.html', {'form': form})


# The user logs out of view

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('rango:index')


# Edit the profile view
def edit_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('rango:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'registration/edit_profile.html', {'profile_form': profile_form})