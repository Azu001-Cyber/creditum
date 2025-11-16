from django import forms
from .models import User

from django import forms
from .models import User


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',"phone", "dob", "gender", "pfp"]

        widgets = {
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. +234 812 345 6789"
            }),
            "dob": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "gender": forms.Select(attrs={
                "class": "form-select"
            }),
            "pfp": forms.FileInput(attrs={
                "class": "form-control"
            }),
        }

        labels = {
            "dob": "Date of Birth",
            "passport": "Passport Photo",
        }

        help_texts = {
            "passport": "Upload a recent passport photograph.",
        }


class FinancialAccountForm(forms.ModelForm):
        document_image = forms.ImageField(required=True, error_messages={
            'required':'Please submit a valid and clear image of the selected document type'
        })
        bvn_number = forms.CharField(required=True, error_messages={
            'required':'Submit a Valid BVN'
        })

        class Meta:
            model = User
            fields = [
                "address",
                "document_type",
                "document_image",
                "bvn_number",
                "tin_number",
            ]

            widgets = {
                "address": forms.Textarea(attrs={
                    "class": "form-control",
                    "placeholder": "Enter residential address",
                    "rows": 3
                }),
                "document_type": forms.Select(attrs={
                    "class": "form-select",
                }),
                "document_image": forms.FileInput(attrs={
                    "class": "form-control"
                }),
                "bvn_number": forms.TextInput(attrs={
                    "class": "form-control",
                    "placeholder": "Enter BVN (11 digits)"
                }),
                "tin_number": forms.TextInput(attrs={
                    "class": "form-control",
                    "placeholder": "Enter TIN if available"
                }),
            }

            labels = {
                "document_type": "Document Type",
                "document_image": "Upload Document",
                "bvn_number" : "Bank Verification Number",
                "tin_number" : "Tax Identification Number",
            }

            help_texts = {
                "document_image": "Upload the selected document (max size: 2MB)",
            }