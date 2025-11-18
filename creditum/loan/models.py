from django.db import models
from account.models import User
from django.utils import timezone
from django.core.mail import send_mail

import string
from random import sample as shuffle
from decimal import Decimal

# Unique transaction id generator
def generate_tid() -> str:
    """
    generates a unique transaction identification
    sequence for any transaction object creation.
    """
    chars = string.ascii_letters + string.digits
    text = shuffle(chars, k=12)
    tid = ''.join(text)
    return tid

# Create your models here.


class LoanSettings(models.Model):
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Default interest rate (%) applied to new loans"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Current Interest Rate: {self.interest_rate}%"

    class Meta:
        get_latest_by = 'updated_at'

class Loan(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"
    STATUS_COMPLETED = "COMPLETED"

    borrower = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_account = models.CharField(null=True, blank=False, max_length=12)
    bank_name = models.CharField(null=True, blank=False, max_length=100)
    bank_code = models.CharField(max_length=10, null=True, blank=False) 
    tenure_months = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=[
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_COMPLETED, "Completed"),
    ] , default='PENDING')

    type = models.CharField(max_length=30, choices=[
        ('personal loan', 'PERSONAL LOAN'),
        ('student loan', 'STUDENT LOAN'),
        ('business loan', 'BUSINESS LOAN'),
    ], default='personal loan')
    reason = models.TextField()

    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Total amout to be payed back PRINCIPEL + INTEREST
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    disbursed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # --- Get old status from DB (if updating) ---
        old_status = None
        if self.pk:
            old_status = Loan.objects.filter(pk=self.pk).values_list("status", flat=True).first()

        # --- Auto-set interest_rate only if not provided ---
        if not self.interest_rate:
            try:
                self.interest_rate = LoanSettings.objects.latest('updated_at').interest_rate
            except LoanSettings.DoesNotExist:
                self.interest_rate = 0.5  # fallback default

            # Calculate totals only if loan is not already approved (freeze on APPROVED/completed)
        if old_status != self.STATUS_APPROVED and old_status != self.STATUS_COMPLETED:
            if self.amount and self.tenure_months:
                interest_rate_decimal = Decimal(str(self.interest_rate)) # Convert via string for precision
                # simple interest:
                interest_amount = (self.amount * interest_rate_decimal * Decimal(self.tenure_months)) / (Decimal(12))
                self.total_payable = self.amount + interest_amount
                self.monthly_installment = self.total_payable / self.tenure_months
                # If remaining_balance is empty (new loan), initialize it to total_payable
                if self.remaining_balance is None or self.remaining_balance == Decimal("0"):
                    self.remaining_balance = self.total_payable

        # When loan status changes to APPROVED from a non-approved state, record disbursed_at
        # (and ensure remaining_balance is set)
        if (old_status != self.STATUS_APPROVED) and (self.status == self.STATUS_APPROVED):
            if self.total_payable and (self.remaining_balance is None):
                self.remaining_balance = self.total_payable
            # mark disbursed time
            if not self.disbursed_at:
                self.disbursed_at = timezone.now()

        super().save(*args, **kwargs)

                # Trigger email when status changes to APPROVED
        if old_status != "APPROVED" and self.status == "APPROVED":
            Transaction.objects.create(
            loan=self,
            borrower=self.borrower,
            amount=self.amount,
            type="DISBURSEMENT",
            tid = generate_tid(),
            narration="Loan approved and disbursed.")
            self.send_approval_email()

    
    def send_approval_email(self):
        message = (
            f"Hello {self.borrower},\n\n"
            f"Your loan request of {self.amount} has been approved.\n"
            f"Loan tenure: {self.tenure_months} months\n"
            f"Interest rate: {self.interest_rate}%\n\n"
            f"Thank you!"
        )

        send_mail(
            subject="Loan Request Approved ✅",
            message=message,
            from_email=None,
            recipient_list=[self.borrower],
            fail_silently=True,
        )



    def __str__(self):
        return f'Loan {self.id} for {self.borrower}'
    

class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            Transaction.objects.create(
                loan=self.loan,
                borrower=self.loan.borrower,
                amount=self.amount,
                type="REPAYMENT",
                tid = generate_tid(),
                narration=f"Loan repayment of {self.amount}"
            )
            
            # self.loan.send_repayment_email(self.amount)

    def send_repayment_email(self, amount):
        message = (
            f"Hello {self.borrower},\n\n"
            f"We received your payment of {amount}.\n"
            f"Your remaining balance is {self.loan.remaining_balance}.\n\n"
            f"Thank you!"
        )

        send_mail(
            subject="Loan Payment Received ✅",
            message=message,
            from_email=None,
            recipient_list=[self.user.email],
            fail_silently=True,
        )

    def __str__(self):
        return f"Repayment {self.id} - loan {self.loan_id} - {self.amount}"
    




class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("DISBURSEMENT", "Disbursement"),
        ("REPAYMENT", "Repayment"),
        ("ADJUSTMENT", "Adjustment"),
    ]

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="transactions")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    tid = models.CharField(max_length=20,unique=True, null=True, blank=True)
    narration = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    @property
    def history(self):
        return self.transactions.all()

    def __str__(self):
        return f"{self.type} - {self.amount} for {self.loan_id} on {self.timestamp}"
