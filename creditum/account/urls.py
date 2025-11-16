
from django.urls import path
from . import views

urlpatterns = [
    path('create/bai', views.account_view, name='basic-account-create'),
    path('create/fai', views.financial_account_view, name='financial-account-create'),
    path('view/profile', views.user_profile_view, name='profile'),
]

