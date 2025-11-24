from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.contrib import messages
from .models import Loan, Repayment, Transaction
from .forms import LoanApplicationForm, RepaymentForm

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import fetch_nigerian_banks
"""
Gets list of banks with a paystack api key
"""
@api_view(["GET"])
def get_banks(request):
    success, result = fetch_nigerian_banks()

    if success:
        return Response({"banks": result}, status=status.HTTP_200_OK)
    return Response({"error": result}, status=status.HTTP_404_NOT_FOUND)



@login_required(login_url='login')
def apply_loan(request):
    if request.method == "POST":
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.borrower = request.user
            # retriving and save bank name from paystack
            bank_code = request.POST.get('bank_code')
            success, banks = fetch_nigerian_banks()
            bank_name = ""
            if success:
                for b in banks:
                    if b["code"] == bank_code:
                        bank_name = b["name"]
                        break
            loan.bank_code = bank_code
            loan.bank_name = bank_name
            # ------------------------
            loan.save()
            return redirect("loan_detail", loan.id)
    else:
        form = LoanApplicationForm()

    return render(request, "loan/apply.html", {"form": form})


@login_required(login_url='login')
def loan_detail(request, pk):
    loan = get_object_or_404(Loan, pk=pk, borrower=request.user)
    return render(request, "loan/loan_detail.html", {"loan": loan})


@login_required(login_url='login')
def repayment_detail(request, pk):
    repay = get_object_or_404(Repayment, pk=pk, loan__borrower=request.user)
    return render(request, 'loan/repayment_detail.html', {'repay':repay})

@login_required(login_url='login')
def make_repayment(request, pk):
    loan = get_object_or_404(Loan, pk=pk, borrower=request.user)

    if loan.status != Loan.STATUS_APPROVED:
        return redirect("loan_detail", pk)

    if request.method == "POST":
        form = RepaymentForm(request.POST)
        if form.is_valid():
            amt = form.cleaned_data["amount"]

            repayment = Repayment.objects.create(
                loan=loan,
                amount=amt)

            # update remaining balance
            loan.remaining_balance -= amt
            if loan.remaining_balance <= 0:
                loan.remaining_balance = 0
                loan.status = Loan.STATUS_COMPLETED

            loan.save()
            return redirect("loan_detail", pk)
    else:
        form = RepaymentForm()

    return render(
        request,
        "loan/repay.html",
        {"form": form, "loan": loan}
    )

"""
Handel all loan history of current user
"""
def loan_history(request):
    user = request.user
    loans = Loan.objects.filter(borrower=user)
    return render(request, "loan/loan_history.html", {"loans": loans})

"""
Handel all repayment history of current user
"""
def repay_history(request):
    user = request.user
    repays = Repayment.objects.filter(loan__borrower=user).order_by('-timestamp')
    return render(request, 'loan/repayment_history.html', {'repays':repays})


"""
Admin Privilage views
"""
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
@login_required
def approve_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)

    if loan.status == loan.STATUS_APPROVED:
        return redirect("loan_detail", pk)

    loan.status = Loan.STATUS_APPROVED
    loan.save()

    return redirect("loan_detail", pk)


# @staff_member_required
# @login_required(login_url='login')
# def search_history(request):
#     query = request.GET.get("query")
#     search_result = []
#     if query:
#         search_result = Transaction.objects.filter(tid__icontains=query)
#         if not search_result:
#             messages.info(request, 'NO transaction history with transaction identification number.')
#     else:
#         messages.warning(request, 'Please enter a tid for search operation')

#     return render(request, '', {'search_result':search_result})


