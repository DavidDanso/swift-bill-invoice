from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ClientCreationForm, InvoiceCreationForm
from django.db.models import Sum
from .utils import paginateInvoice, calculate_currency_totals
from django.db.models import Sum
from datetime import datetime


# Create your views here.
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
    
    # Retrieve and print the paid dates for invoices in the current month
    current_month = datetime.now().month  # Get the current month
    paid_dates = []  # Initialize a list to store paid dates

    # Iterate through invoices to find those paid in the current month
    for invoice in invoices:
        if invoice.paid_date and invoice.paid_date.month == current_month:
            paid_dates.append(invoice.paid_date)  # Add the paid date to the list
            print(invoice.paid_date)  # Print the paid date for reference


    # Calculate currency totals for paid and pending invoices
    paid_total_usd, pending_total_usd = calculate_currency_totals(invoices)

    data = [1200, 340, 0, 1450, 1200, 3000, 5000]
    labels = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    context = {
        'clients_num': clients_num, 'invoices_num': invoices_num, 
        'paid_total_usd': paid_total_usd, 'pending_total_usd': pending_total_usd, 'clients': clients,
        'data': data, 'labels': labels
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

    # Calculate days until due for each invoice
    for invoice in invoices:
        invoice.due = (invoice.payment_date - datetime.now().date()).days

    # Filter clients based on the current user
    form = InvoiceCreationForm(request.user, request.POST, request.FILES if request.method == "POST" else None)

    if request.method == "POST":
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.account_owner = profile
            invoice.save()

            messages.success(request, 'Invoice created! Click [view invoice] to add items and calculate amount.📝')
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
    # 
    display_items = invoice.items.all()
    items_total = invoice.items.aggregate(total=Sum('total'))['total']

    form = InvoiceCreationForm(request.user, instance=invoice)
    # 
    if request.method == 'POST':
        if 'updateInvoice' in request.POST:
            form = InvoiceCreationForm(request.user, request.POST or None, request.FILES or None, instance=invoice)
            if form.is_valid():
                form.save()

                # Check if the invoice is paid, and update the payment_date
                if invoice.invoice_status == 'Paid':
                    invoice.paid_date = datetime.now().date()
                    invoice.save()
                return redirect('invoice')
            
        elif 'addItem' in request.POST:
            item = Item.objects.create(
                account_owner = profile,
                title = request.POST.get('title'),
                quantity = request.POST.get('quantity'),
                price = request.POST.get('price'),
                invoice = invoice,
            )
            return redirect('invoice-details', pk=invoice.id)
        
        elif "deleteItem" in request.POST:
            item_id = request.POST.get('deleteItem')

            item_to_delete = invoice.items.get(id=item_id)
            item_to_delete.delete()
            # Redirect to the same page after deletion
            return redirect('invoice-details', pk=invoice.id)
        
        elif "delete_invoice" in request.POST:
            invoice.delete()
            return redirect('invoice')

    context = {
        'form': form,
        'invoice': invoice, 
        'display_items': display_items,
        'items_total': items_total,
    }
    return render(request, 'invoice/invoice-details.html', context)


########################################## preview-invoice page views
@login_required(login_url='login')
def preview_invoice(request, pk):
    profile = request.user.profile
    invoice = profile.invoice_set.get(id=pk)

    items = invoice.items.all()
    items_total = invoice.items.aggregate(total=Sum('total'))['total']

    context = {'invoice': invoice, 'profile': profile, 'items': items, 
               'items_total': items_total}
    return render(request, 'invoice/preview-invoice.html', context)



########################################## add-invoice items page views
# def add_invoiceItems(request):
#     profile = request.user.profile
#     # Filter clients based on the current user
#     form = InvoiceCreationForm(request.user, request.POST, request.FILES if request.method == "POST" else None)

#     if request.method == "POST":
#         if form.is_valid():
#             invoice = form.save(commit=False)
#             invoice.account_owner = profile
#             invoice.save()
#             context = {'invoice': invoice}
#             return render(request, 'invoice/add-items.html', context)
#         else:
#             messages.error(request, 'Invalid form: Please check and resubmit')

#     context = {'form': form}
#     return render(request, 'invoice/add-items.html', context)


