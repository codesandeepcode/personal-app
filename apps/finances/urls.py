from django.urls import path

from .views import BankAccountListView, TransactionListView

urlpatterns = [
    path("bank-accounts/", BankAccountListView.as_view(), name="bank_accounts"),
    path("transactions/", TransactionListView.as_view(), name="transactions"),
]