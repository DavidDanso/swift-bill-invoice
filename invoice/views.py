from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ClientCreationForm, InvoiceCreationForm
from django.db.models import Sum


# Create your views here.
########################################## home page views
def homePage(request):
    return HttpResponse("<h1>Index page under construction 🚧🦺.</h1>")

########################################## dashboard page views
@login_required(login_url='login')
def dashboardPage(request):
    profile = request.user.profile
    clients = profile.client_set.all()
    clients_num = clients.count()

    invoices = profile.invoice_set.all()
    invoices_num = invoices.count()

    pending_invoice = profile.invoice_set.filter(invoice_status='Pending').aggregate(Sum('total'))['total__sum']
    paid_invoice = profile.invoice_set.filter(invoice_status='Paid').aggregate(Sum('total'))['total__sum']

    context = {'clients_num': clients_num, 'invoices_num': invoices_num, 
               'pending_invoice': pending_invoice, 'paid_invoice': paid_invoice, 'clients': clients}
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

    # Filter clients based on the current user
    form = InvoiceCreationForm(request.user, request.POST, request.FILES if request.method == "POST" else None)

    if request.method == "POST":
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.account_owner = profile
            invoice.save()
        else:
            messages.error(request, 'Invalid form: Please check and resubmit')

    context = {'form': form, 'invoices': invoices}
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