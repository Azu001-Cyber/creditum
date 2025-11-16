# loans/forms.py
from django import forms
from .models import Loan

from django import forms
from .models import Loan

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = [
            "amount", "bank_account", "bank_name",
            "tenure_months", "type", "reason"
        ]
        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter loan amount"
            }),
            "bank_account": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter bank account number"
            }),
            "bank_name": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Select a bank"
            }),
            "tenure_months": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter loan tenure in months"
            }),
            "type": forms.Select(attrs={
                "class": "form-select"
            }),
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Reason for taking the loan",
                "rows": 3
            }),
        }


class RepaymentForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter repayment amount"
        })
    )
