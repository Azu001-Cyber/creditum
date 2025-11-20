
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.UserDashboardView, name='user-dashboard'),
    path('loans/<int:loan_id>/repay/', views.RepaymentView.as_view(), name='repay-loan'),
]
