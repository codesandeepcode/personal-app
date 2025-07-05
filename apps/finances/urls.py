from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BankAccountListCreateView,
    BankAccountDetailView,
    TransactionListCreateView,
    TransactionDetailView,
    transaction_list_view,
    transaction_create_view,
    TransferViewSet,
    TransactionSummaryView,
    InvestmentViewSet,
)

router = DefaultRouter()
router.register(r'transfers', TransferViewSet, basename='transfer')
router.register(r'investments', InvestmentViewSet, basename='investment')

urlpatterns = [
    path("bank-accounts/", BankAccountListCreateView.as_view(), name="bankaccount-list-create"),
    path("bank-accounts/<uuid:pk>/", BankAccountDetailView.as_view(), name="bankaccount-detail"),
    path("transactions/", TransactionListCreateView.as_view(), name="transaction-list-create"),
    path("transactions/<uuid:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
    path('web/transactions/', transaction_list_view, name='transaction_list'),
    path('web/transactions/add/', transaction_create_view, name='transaction_create'),
    path('', include(router.urls)),
    path('transactions/summary/', TransactionSummaryView.as_view(), name='transaction_summary'),
]