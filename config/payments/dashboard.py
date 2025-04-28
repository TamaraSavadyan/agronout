from .models import PaymentAttempt, Invoice


def create_payment_attempt(invoice: Invoice, amount: float) -> PaymentAttempt:
    if invoice.status == Invoice.Status.EXPIRED:
        result = PaymentAttempt.Result.DECLINED
    elif amount < invoice.amount:
        result = PaymentAttempt.Result.INSUFFICIENT_FUNDS
    else:
        result = PaymentAttempt.Result.SUCCESS
        invoice.status = Invoice.Status.PAID
        invoice.save()

    return PaymentAttempt.objects.create(
        invoice=invoice,
        amount=amount,
        result=result,
    )


