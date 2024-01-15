from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from .forms import ClientCreationForm, InvoiceCreationForm
from django.db.models import Sum
from .utils import paginateInvoice

    
# Create your views here.
########################################## home page views
def homePage(request):
    return HttpResponse("<h1>Index page under construction 🚧🦺.</h1>")

########################################## dashboard page views
@login_required(login_url='login')
def dashboard_page(request):
    profile = request.user.profile

    # Clients
    clients = profile.client_set.all()
    clients_num = clients.count()

    # Invoices
    invoices = profile.invoice_set.all()
    invoices_num = invoices.count()

    # Currencies and Exchange Rates
    currency_rates = {
        'NGN': 0.00104407,
        'GHS': 0.0836498,
        'GBP': 1.27777,
        'EUR': 1.09799,
        'USD': 1.00000,
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

    context = {
        'clients_num': clients_num, 'invoices_num': invoices_num, 
        'paid_total_usd': paid_total_usd, 'pending_total_usd': pending_total_usd, 'clients': clients,
    }

    return render(request, 'invoice/dashboard.html', context)


########################################## client page views
@login_required(login_url='login')
def create_client(request):
    profile = request.user.profile
    clients = profile.client_set.all()
    form = ClientCreationForm()

    # 
    if request.method == "POST":
        form = ClientCreationForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save(commit=False)
            client.account_owner = profile
            client.save()
            # client creation success message
            messages.success(request,  'Client created Successful✅')
            return redirect('clients')
        else:
            messages.error(request,  'Invalid form: Please check and resubmit')


    context = {'form': form, 'clients': clients}
    return render(request, 'invoice/client.html', context)


########################################## client-details page views
@login_required(login_url='login')
def edit_client(request, pk):
    profile = request.user.profile
    client = profile.client_set.get(id=pk)
    form = ClientCreationForm(instance=client)

    # 
    if request.method == "POST":
        form = ClientCreationForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            # client update success message
            messages.success(request,  'Client updated Successful✅')
            return redirect('clients')
        elif "delete_client" in request.POST:
            client.delete()
            # client deletion success message
            messages.success(request,  'Client deleted Successful👤')
            return redirect('clients')
        
    context = {'form': form, 'client': client}
    return render(request, 'invoice/client-details.html', context)


########################################## invoice page views
@login_required(login_url='login')
def create_invoice(request):
    profile = request.user.profile
    invoices = profile.invoice_set.all()

    custom_range, invoices = paginateInvoice(request, 5, invoices)

    # Filter clients based on the current user
    form = InvoiceCreationForm(request.user, request.POST, request.FILES if request.method == "POST" else None)

    if request.method == "POST":
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.account_owner = profile
            invoice.save()
            return redirect('invoice')
        else:
            messages.error(request, 'Invalid form: Please check and resubmit')

    context = {'form': form, 'invoices': invoices,
               'custom_range': custom_range}
    return render(request, 'invoice/invoice.html', context)


########################################## edit-invoice page views
@login_required(login_url='login')
def edit_invoice(request, pk):
    profile = request.user.profile
    invoice = profile.invoice_set.get(id=pk)

    form = InvoiceCreationForm(request.user, request.POST or None, request.FILES or None, instance=invoice)

    # 
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('invoice')
        elif "delete_invoice" in request.POST:
            invoice.delete()
            return redirect('invoice')

    context = {
        'form': form,
        'invoice': invoice, 
    }
    return render(request, 'invoice/invoice-details.html', context)


########################################## preview-invoice page views
@login_required(login_url='login')
def preview_invoice(request, pk):
    profile = request.user.profile
    invoice = profile.invoice_set.get(id=pk)

    context = {'invoice': invoice, 'profile': profile}
    return render(request, 'invoice/preview-invoice.html', context)