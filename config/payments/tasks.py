from celery import shared_task
from django.utils import timezone
from .models import Invoice


@shared_task
def expire_invoice(invoice_id: int) -> None:
    from .models import Invoice

    invoice = Invoice.objects.get(id=invoice_id)
    if invoice.status == Invoice.Status.WAITING and invoice.due_date <= timezone.now():
        invoice.status = Invoice.Status.EXPIRED
        invoice.save()
