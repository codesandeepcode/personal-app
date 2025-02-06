from django.db import models
from apps.accounts.models import UserData

from apps.models import BaseModel


class BankAccount(BaseModel):
    bank_name = models.CharField(max_length=100)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "categories"

    
class SubCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name_plural = "sub-categories"


class Transaction(BaseModel):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSACTION_TYPE_CHOICES = (
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    )

    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES, default=EXPENSE)
    description = models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    sub_category = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.SET_NULL)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_date = models.DateField()

    def __str__(self):
        return f"{self.bank_account.name} - {self.amount} - {self.description}"


class FixedExpense(BaseModel):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"
    FRQUENCY_CHOICES = (
        (MONTHLY, "Monthly"),
        (QUARTERLY, "Quarterly"),
        (ANNUALLY, "Annually"),
    )
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    due_date = models.DateField()
    frequency = models.CharField(max_length=50, choices=FRQUENCY_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.frequency})"


class Investment(BaseModel):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    investment_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.current_value}"


class Borrowing(BaseModel):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount_borrowed = models.DecimalField(max_digits=15, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    lender = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.amount_borrowed} ({self.lender})"
    

class Plan(BaseModel):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    target_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.target_amount} ({self.target_date})"
