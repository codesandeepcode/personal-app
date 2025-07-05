from django.db import models

from apps.models import BaseModel
from apps.users.models.user import User


class BankAccount(BaseModel):
    account_name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bank_accounts"
    )
    account_number = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.account_name} - {self.bank_name}"


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "categories"


class SubCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories"
    )

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name_plural = "sub-categories"


class Transaction(BaseModel):
    DEPOSIT = "INCOME"
    WITHDRAWAL = "EXPENSE"
    TRANSFER = "TRANSFER"
    PAYMENT = "PAYMENT"

    TRANSACTION_TYPES = [
        (DEPOSIT, "Deposit"),
        (WITHDRAWAL, "Withdrawal"),
        (TRANSFER, "Transfer"),
        (PAYMENT, "Payment"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPES, default=PAYMENT
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    sub_category = models.ForeignKey(
        SubCategory, null=True, blank=True, on_delete=models.SET_NULL
    )
    transfer = models.ForeignKey(
        "Transfer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.date}"


class Transfer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transfers")
    source_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, related_name="transfers_out"
    )
    destination_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, related_name="transfers_in"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateTimeField()

    def __str__(self):
        return f"Transfer of {self.amount} from {self.source_account} to {self.destination_account} on {self.date}"


class RecurringTransaction(BaseModel):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"
    FREQUENCY_CHOICES = (
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
        (QUARTERLY, "Quarterly"),
        (ANNUALLY, "Annually"),
    )

    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recurring_transactions"
    )
    account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, related_name="recurring_transactions"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=Transaction.TRANSACTION_TYPES,
        default=Transaction.PAYMENT,
    )
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_processed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} ({self.frequency})"


class Investment(BaseModel):
    STOCK = "STOCK"
    BOND = "BOND"
    MUTUAL_FUND = "MUTUAL_FUND"
    ETF = "ETF"
    REAL_ESTATE = "REAL_ESTATE"
    CRYPTO = "CRYPTO"
    GOLD = "GOLD"
    OTHER = "OTHER"

    INVESTMENT_TYPES = [
        (STOCK, "Stock"),
        (BOND, "Bond"),
        (MUTUAL_FUND, "Mutual Fund"),
        (ETF, "Exchange-Traded Fund"),
        (REAL_ESTATE, "Real Estate"),
        (CRYPTO, "Cryptocurrency"),
        (GOLD, "Gold"),
        (OTHER, "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="investments")
    investment_type = models.CharField(
        max_length=20, choices=INVESTMENT_TYPES, default=STOCK
    )
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, blank=True)
    purchase_date = models.DateField()
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    current_price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} - ({self.investment_type})"

    @property
    def profit_loss(self):
        if self.current_value and self.purchase_price and self.quantity:
            return (self.current_price - self.purchase_price) * self.quantity
        return None


class Borrowing(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount_borrowed = models.DecimalField(max_digits=15, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    lender = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.amount_borrowed} ({self.lender})"


class Plan(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    target_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.target_amount} ({self.target_date})"
