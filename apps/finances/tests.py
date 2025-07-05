from django.test import TestCase
from apps.accounts.models import User
from .models import BankAccount, Transaction, Transfer

class TransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@mail.in',
            password='testpassword',
        )
        self.bank_account = BankAccount.objects.create(
            account_name='Test Account',
            bank_name='Test Bank',
            account_number='123456789',
            user=self.user,
            balance=1000.00
        )

    def test_create_transaction(self):
        transaction = Transaction.objects.create(
            bank_account=self.bank_account,
            amount=100.00,
            transaction_type='credit',
            description='Test Transaction',
            date='2023-10-01T00:00:00Z',
            user=self.user
        )
        self.assertEqual(transaction.bank_account, self.bank_account)
        self.assertEqual(transaction.amount, 100.00)
        self.assertEqual(transaction.transaction_type, 'credit')
        self.assertEqual(transaction.description, 'Test Transaction')
        self.assertEqual(transaction.user, self.user)


class TransferTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@email.in', password='12345')
        self.account1 = BankAccount.objects.create(user=self.user, account_name='A1', account_number='123', bank_name='Test', balance=1000)
        self.account2 = BankAccount.objects.create(user=self.user, account_name='A2', account_number='456', bank_name='Test', balance=500)

    def test_transfer_success(self):
        transfer = Transfer.objects.create(
            user=self.user,
            source_account=self.account1,
            destination_account=self.account2,
            amount=200,
            description='Test transfer'
        )
        Transaction.objects.create(
            user=self.user,
            account=self.account1,
            amount=-200,
            transaction_type='TRANSFER',
            transfer=transfer
        )
        Transaction.objects.create(
            user=self.user,
            account=self.account2,
            amount=200,
            transaction_type='TRANSFER',
            transfer=transfer
        )
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account1.balance, 800)
        self.assertEqual(self.account2.balance, 700)
