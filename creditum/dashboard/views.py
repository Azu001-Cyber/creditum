from django.shortcuts import render
from account.models import User
from loan.models import Loan, Repayment, Transaction

# Create your views here.

def UserDashboardView(request):
    user = request.user
    loan_data = Loan.objects.filter(borrower=user)
    repayment_data = Repayment.objects.filter(loan__in=loan_data)
    transaction_data = Transaction.objects.filter(borrower=user)


    context = {
            'user_info':user,
            'loan_info':loan_data,
            'repayment_info':repayment_data,
            'txn_info':transaction_data
        }
    
    return render(request, 'dashboard/user_dashboard.html', context)