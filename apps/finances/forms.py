from django import forms

from .models import BankAccount, Category, Transaction, Transfer


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


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ["source_account", "destination_account", "amount", "description"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['source_account'].queryset = BankAccount.active_objects.filter(user=user)
        self.fields['destination_account'].queryset = BankAccount.active_objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        source_account = cleaned_data.get("source_account")
        destination_account = cleaned_data.get("destination_account")
        amount = cleaned_data.get("amount")

        if source_account and destination_account and source_account == destination_account:
            raise forms.ValidationError("Source and destination accounts cannot be the same.")

        if source_account and amount and source_account.balance < amount:
            raise forms.ValidationError("Insufficient funds in the source account.")

        return cleaned_data
