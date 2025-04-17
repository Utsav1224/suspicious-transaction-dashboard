from django.db import models

class SuspiciousTransaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    account_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    rule_triggered = models.CharField(max_length=255)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"
