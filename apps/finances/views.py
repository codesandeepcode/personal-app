from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django.db import transaction as db_transaction
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.db.models import Sum

from .models import BankAccount, Transaction, Transfer
from .serializers import BankAccountSerializer, TransactionSerializer, TransferSerializer
from .forms import TransactionForm


class BankAccountListCreateView(generics.ListCreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccount.active_objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccount.active_objects.filter(user=self.request.user)
    

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transaction_type', 'category', 'subcategory', 'date']

    def get_queryset(self):
        return Transaction.active_objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.active_objects.filter(user=self.request.user)


@login_required
def transaction_list_view(request):
    transactions = Transaction.active_objects.filter(user=request.user)
    return render(request, 'finances/transaction_list.html', {'transactions': transactions})

@login_required
def transaction_create_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm()
    return render(request, 'finances/transaction_form.html', {'form': form})


class TransferViewSet(viewsets.ModelViewSet):
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transfer.active_objects.filter(user=self.request.user)

    @db_transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transfer = serializer.save(user=request.user)

        # Create withdrawal transaction for source account
        Transaction.objects.create(
            user=request.user,
            bank_account=transfer.source_account,
            amount=transfer.amount,
            transaction_type=Transaction.TRANSFER,
            description=transfer.description,
            date=transfer.date,
            transfer=transfer
        )

        # Create deposit transaction for destination account
        Transaction.objects.create(
            user=request.user,
            bank_account=transfer.destination_account,
            amount=transfer.amount,
            transaction_type=Transaction.TRANSFER,
            description=transfer.description,
            date=transfer.date,
            transfer=transfer
        )

        # Update balances
        transfer.source_account.balance -= transfer.amount
        transfer.source_account.save()
        transfer.destination_account.balance += transfer.amount
        transfer.destination_account.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        transactions = Transaction.active_objects.filter(user=request.user)
        if start_date and end_date:
            transactions = transactions.filter(date__range=[start_date, end_date])
        
        total_deposits = transactions.filter(transaction_type=Transaction.DEPOSIT).aggregate(total=Sum('amount'))['total'] or 0
        total_withdrawals = transactions.filter(transaction_type=Transaction.WITHDRAWAL).aggregate(total=Sum('amount'))['total'] or 0
        total_transfers = transactions.filter(transaction_type=Transaction.TRANSFER, amount__gt=0).aggregate(total=Sum('amount'))['total'] or 0

        net_change = total_deposits - total_withdrawals

        return Response({
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'total_transfers': total_transfers,
            'net_change': net_change
        }, status=status.HTTP_200_OK)

