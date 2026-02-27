from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from App_Login.forms import SignUpForm, UserProfileChange, ProfilePic
from App_Login.models import UserProfile


def sign_up(request):
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
    context = {'form': form, 'registered': registered}
    return render(request, 'App_Login/signup.html', context=context)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    return render(request, 'App_Login/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:signin'))


@login_required
def profile(request):
    has_profile = UserProfile.objects.filter(user=request.user).exists()
    return render(request, 'App_Login/profile.html', context={'has_profile': has_profile})


@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            form = UserProfileChange(instance=current_user)
    return render(request, 'App_Login/change_profile.html', context={'form': form})


@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)

    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            changed = True
            messages.success(request, 'Password changed successfully!')

    return render(request, 'App_Login/pass_change.html', context={'form': form, 'changed': changed})


@login_required
def add_pro_pic(request):
    form = ProfilePic()
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html', context={'form': form})


@login_required
def change_pro_pic(request):
    try:
        user_profile = request.user.user_profile
    except UserProfile.DoesNotExist:
        return redirect('App_Login:add_pro_pic')

    form = ProfilePic(instance=user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html', context={'form': form})
