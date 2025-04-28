from django.db import models
from django.utils import timezone
from typing import Self

class Invoice(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "Ожидает оплату"
        PAID = "paid", "Оплачен"
        EXPIRED = "expired", "Просрочен"

    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    status: models.CharField = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING,
    )
    due_date: models.DateTimeField = models.DateTimeField()

    def __str__(self) -> str:
        return f"Invoice #{self.id} - {self.status}"


class PaymentAttempt(models.Model):
    class Result(models.TextChoices):
        SUCCESS = "success", "Успешно"
        INSUFFICIENT_FUNDS = "insufficient_funds", "Недостаточно средств"
        DECLINED = "declined", "Отказ"

    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    result: models.CharField = models.CharField(
        max_length=20,
        choices=Result.choices,
    )
    invoice: models.ForeignKey = models.ForeignKey(
        Invoice, related_name="payment_attempts", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"PaymentAttempt #{self.id} - {self.result}"
