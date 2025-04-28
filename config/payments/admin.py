from django.contrib import admin
from .models import Invoice, PaymentAttempt
from django.utils.html import format_html
from django_unfold.admin import ModelAdmin as UnfoldModelAdmin # type: ignore


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "created_at", "status_colored", "due_date")
    list_filter = ("status",)

    def status_colored(self, obj: Invoice) -> str:
        color_map = {
            "waiting": "orange",
            "paid": "green",
            "expired": "red",
        }
        color = color_map.get(obj.status, "black")
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())

    status_colored.short_description = "Статус"


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "created_at", "result_colored", "invoice")
    list_filter = ("result",)

    def result_colored(self, obj: PaymentAttempt) -> str:
        color_map = {
            "success": "green",
            "insufficient_funds": "orange",
            "declined": "red",
        }
        color = color_map.get(obj.result, "black")
        return format_html('<span style="color: {};">{}</span>', color, obj.get_result_display())

    result_colored.short_description = "Результат"
