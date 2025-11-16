from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

# password management urls endpoint
urlpatterns += [
    path('password/reset/', 
        auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'),
        name='reset_password'
        ),

    path('password/reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'),
        name='password_reset_done'
        ),

    path('password/reset/comfirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),
        name='password_reset_confirm'
        ),

    path('password/reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
        name='password_reset_complete'
        )
]