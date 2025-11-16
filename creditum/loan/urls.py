from django.urls import path
from . import views

urlpatterns = [
    path("banks/", views.get_banks, name="banks-list"),
    path("apply/", views.apply_loan, name="apply_loan"),
    path("detail/<int:pk>/", views.loan_detail, name="loan_detail"),
    path('detail/repay/<int:pk>/', views.repayment_detail, name='repay_detail'),
    path("<int:pk>/approve/", views.approve_loan, name="approve_loan"),
    path("<int:pk>/repay/", views.make_repayment, name="make_repayment"),
    path('history/', views.loan_history, name='loan_history'),
    path('repayment/history/', views.repay_history, name='repay_history'),
]