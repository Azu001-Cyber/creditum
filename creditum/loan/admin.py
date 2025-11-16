from django.contrib import admin
from . models import Loan, LoanSettings, Transaction, Repayment
# Register your models here.
admin.site.register(Loan)
admin.site.register(LoanSettings)
admin.site.register(Transaction)
admin.site.register(Repayment)