from rest_framework import serializers

from .models import BankAccount, Category, SubCategory, Transaction, FixedExpense, Investment, Borrowing, Plan


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        exclude = ("id", "created_at", "updated_at",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id", "created_at", "updated_at",)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        exclude = ("id", "created_at", "updated_at",)


class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()

    class Meta:
        model = Transaction
        exclude = ("id", "created_at", "updated_at",)


class FixedExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedExpense
        exclude = ("id", "created_at", "updated_at",)


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        exclude = ("id", "created_at", "updated_at",)


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        exclude = ("id", "created_at", "updated_at",)


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        exclude = ("id", "created_at", "updated_at",)
