from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from datetime import datetime

# 
def paginateInvoice(request, results, invoices):
    page = request.GET.get('page')
    results = results
    paginator = Paginator(invoices, results)

    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        invoices = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        invoices = paginator.page(page)

    # 
    leftIndex = (int(page) -4)
    if leftIndex < 1:
        leftIndex = 1

    # 
    rightIndex = (int(page) +5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, invoices


def calculate_currency_totals(invoices):
    # Currencies and Exchange Rates
    currency_rates = {
        'NGN 🇳🇬': 0.000712758,
        'GHS 🇬🇭': 0.0811322, 
        'GBP 🇬🇧': 1.25401,
        'EUR 🇪🇺': 1.07450,
        'USD 🇺🇸': 1.00000,
    }

    # Invoice Status by Currency
    pending_invoices_by_currency = {}
    paid_invoices_by_currency = {}

    for currency, rate in currency_rates.items():
        pending_total = invoices.filter(currency=currency, invoice_status='Pending').aggregate(Sum('total'))['total__sum'] or 0
        paid_total = invoices.filter(currency=currency, invoice_status='Paid').aggregate(Sum('total'))['total__sum'] or 0

        pending_invoices_by_currency[currency] = pending_total
        paid_invoices_by_currency[currency] = paid_total

    # Convert Amount to USD
    def convert_to_usd(amount, rate):
        return amount * rate

    paid_total_usd = sum(convert_to_usd(amount, currency_rates[currency]) for currency, amount in paid_invoices_by_currency.items())
    pending_total_usd = sum(convert_to_usd(amount, currency_rates[currency]) for currency, amount in pending_invoices_by_currency.items())

    return paid_total_usd, pending_total_usd