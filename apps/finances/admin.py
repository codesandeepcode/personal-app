from django.contrib import admin

from .models import BankAccount, Category, SubCategory, Transaction, RecurringTransaction, Investment, Borrowing, Plan

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'bank_name', 'balance', 'user')
    search_fields = ('account_name', 'bank_name', 'account_number')
    list_filter = ('user', 'bank_name')


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Transaction)
admin.site.register(RecurringTransaction)
admin.site.register(Investment)
admin.site.register(Borrowing)
admin.site.register(Plan)
