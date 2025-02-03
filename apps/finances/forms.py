from django import forms

from .models import Bank, BankBalance, Category, Transaction


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ["name"]


class BankBalanceForm(forms.ModelForm):
    class Meta:
        model = BankBalance
        fields = ["bank", "balance"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["bank", "category", "amount", "reason", "date", "is_debit"]
