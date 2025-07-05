from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.finances.models import RecurringTransaction, Transaction

class Command(BaseCommand):
    help = 'Process recurring transactions'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        for rt in RecurringTransaction.active_objects.filter(start_date__lte=today, end_date__gte=today):
            if not rt.last_processed or self.should_process(rt, today):
                Transaction.objects.create(
                    user=rt.user,
                    bank_account=rt.account,
                    amount=rt.amount,
                    transaction_type=rt.transaction_type,
                    description=rt.description
                )
                rt.last_processed = today
                rt.save()
                self.stdout.write(f"Processed: {rt}")

    def should_process(self, rt, today):
        delta = today - rt.last_processed
        if rt.frequency == RecurringTransaction.DAILY:
            return delta.days >= 1
        elif rt.frequency == RecurringTransaction.WEEKLY:
            return delta.days >= 7
        elif rt.frequency == RecurringTransaction.MONTHLY:
            return delta.days >= 30
        elif rt.frequency == RecurringTransaction.QUARTERLY:
            return delta.days >= 90
        elif rt.frequency == RecurringTransaction.YEARLY:
            return delta.days >= 365
        return False