from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
# your function

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from account.models import User
from django.utils.encoding import force_str
from .emails import send_verification_email

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # deactivate account until email verification
            user.save()

            # Send verification email
            send_verification_email(request, user)

            # Optionally show a page telling the user to check email
            return render(request, "authentication/registration_pending.html", {
                "email": user.email
            })
    else:
        form = RegisterForm()

    return render(request, "authentication/register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'authentication/activation_invalid.html')
    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)  # login the user
                    return redirect('home')    # redirect after successful login
                else:
                    form.add_error(None, "Please verify your email before logging in.")
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')