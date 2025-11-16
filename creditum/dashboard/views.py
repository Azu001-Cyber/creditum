from django.shortcuts import render, get_object_or_404
from account.models import User
from loan.models import Loan, Repayment, Transaction

# Create your views here.

def UserDashboardView(request):
    loan_data = Loan.objects.filter(borrower=request.user)
    repayment_data = Repayment.objects.filter(loan__in=loan_data)
    transaction_data = Transaction.objects.filter(borrower=request.user)


    context = {
            'user_info': request.user,
            'loan_info':loan_data,
            'repayment_info':repayment_data,
            'txn_info':transaction_data
        }
    
    return render(request, 'dashboard/user_dashboard.html', context)