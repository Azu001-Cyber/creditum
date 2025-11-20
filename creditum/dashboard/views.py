from django.shortcuts import render
from account.models import User
from loan.models import Loan, Repayment, Transaction

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import RepaymentSerializer
from django.utils import timezone
from decimal import Decimal
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




class RepaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, loan_id):
        #  Get repayment amount from request
        amount = request.data.get("amount")
        if not amount:
            return Response({"error": "Repayment amount is required."},
                        status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError
        except:
            return Response({"error": "Invalid repayment amount."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch loan
        try:
            loan = Loan.objects.get(id=loan_id, user=request.user)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found."}, 
                            status=status.HTTP_404_NOT_FOUND)

        # Optional: prevent overpayment
        if amount > loan.remaining_balance:
            return Response({"error": "Repayment exceeds loan balance."}, status=status.HTTP_400_BAD_REQUEST)

        #  Call your existing repayment logic
        # (reduce remaining_balance, mark paid, save repayment record)
        loan.remaining_balance -= amount
        if loan.remaining_balance == 0:
            loan.status = "paid"
        loan.save()

        serializer = RepaymentSerializer(data={'loan':loan.id, 'amount':amount})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return response
        return Response({
            "message": "Repayment successful",
            "repayment": serializer.data,
            "remaining_balance": loan.remaining_balance,
            "status": loan.status
        }, status=status.HTTP_201_CREATED)
