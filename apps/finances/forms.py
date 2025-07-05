from django import forms

from .models import BankAccount, Category, Transaction


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["account_name"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["bank_account", "amount", "transaction_type", "description"]
