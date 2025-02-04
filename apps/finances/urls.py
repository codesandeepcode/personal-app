from django.urls import path

from .views import BankAccountListCreateView, BankAccountRetrieveUpdateDestroyView, TransactionListView

urlpatterns = [
    path("bank-accounts/", BankAccountListCreateView.as_view(), name="bank_account_list_create"),
    path("bank-accounts/<uuid:pk>/", BankAccountRetrieveUpdateDestroyView.as_view(), name="bank_account_retrieve_update_destroy"),
    path("transactions/", TransactionListView.as_view(), name="transactions"),
]