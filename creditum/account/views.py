from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AccountForm, FinancialAccountForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from . models import User
# Create your views here.

@login_required(login_url='login')
def account_view(request):
    user = request.user

    if request.method == "POST":
        form = AccountForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account details updated successfully.")
            return redirect('financial-account-create',)
    else:
        form = AccountForm(instance=user)

    return render(request, "account/account.html", {"form": form})



@login_required(login_url='login')
def financial_account_view(request):
    user = request.user

    if request.method == "POST":
        form = FinancialAccountForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Financial details updated.")
            return redirect('profile', email=user.email)
    else:
        form = FinancialAccountForm(instance=user)

    return render(request, "account/financial_account.html", {"form": form})

@require_GET
@login_required(login_url='login')
def user_profile_view(request):
    user = request.user
    try:
        user_profile = user
        has_profile = True
    except User.DoesNotExist:
        user_profile = None
        has_profile = False

    context = {
        "user_info": user_profile,
        'has_profile': has_profile
    }

    return render(request, "account/profile.html", context)
