from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import BankAccount, Category, SubCategory, Transaction, FixedExpense, Investment, Borrowing, Plan
from .serializers import BankAccountSerializer, CategorySerializer, SubCategorySerializer, TransactionSerializer, FixedExpenseSerializer, InvestmentSerializer, BorrowingSerializer, PlanSerializer


class BankAccountListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bank_accounts = BankAccount.objects.filter(user=request.user)
        serializer = BankAccountSerializer(bank_accounts, many=True)
        return Response(serializer.data)
    

class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
