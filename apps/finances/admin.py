from django.contrib import admin

from .models import BankAccount, Category, SubCategory, Transaction, FixedExpense, Investment, Borrowing, Plan

admin.site.register(BankAccount)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Transaction)
admin.site.register(FixedExpense)
admin.site.register(Investment)
admin.site.register(Borrowing)
admin.site.register(Plan)
