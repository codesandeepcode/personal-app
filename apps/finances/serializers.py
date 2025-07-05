from .models import (
    BankAccount,
    Borrowing,
    Category,
    Investment,
    Plan,
    RecurringTransaction,
    SubCategory,
    Transaction,
    Transfer,
)
from rest_framework import serializers


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            "id",
            "account_name",
            "account_number",
            "bank_name",
            "balance",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "bank_account",
            "amount",
            "transaction_type",
            "description",
            "category",
            "subcategory",
            "date",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [
            "id",
            "source_account",
            "destination_account",
            "amount",
            "description",
            "date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        if attrs["source_account"] == attrs["destination_account"]:
            raise serializers.ValidationError(
                "Source and destination accounts cannot be the same."
            )
        if attrs["source_account"].balance < attrs["amount"]:
            raise serializers.ValidationError(
                "Insufficient funds in the source account."
            )
        if (
            attrs["source_account"].user != self.context["request"].user
            or attrs["destination_account"].user != self.context["request"].user
        ):
            raise serializers.ValidationError(
                "Source and destination accounts must belong to the user."
            )
        return attrs


class RecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransaction
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = (
            "id",
            "name",
            "investment_type",
            "symbol",
            "purchase_date",
            "quantity",
            "purchase_price",
            "current_price",
            "profit_loss",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "profit_loss",
        )


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )
