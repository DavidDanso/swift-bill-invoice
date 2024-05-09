from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ClientCreationForm, InvoiceCreationForm
from django.db.models import Sum
from .utils import paginateInvoice, calculate_currency_totals
from django.db.models import Sum
from django.http import HttpResponse
from datetime import datetime
from django.template.loader import render_to_string
from weasyprint import HTML


# Create your views here.
########################################## dashboard page views
@login_required(login_url='login')
def dashboard_page(request):
    profile = request.user.profile

    # Clients
    clients = profile.client_set.all()
    clients_num = clients.count()

    # Invoices
    invoices = profile.acc_user.all()
    invoices_num = invoices.count()
    
    # Assuming invoices is a queryset of Invoice model
    current_month = datetime.now().month # Get the current month
    total_paid_in_current_month_usd = 0  # Initialize a variable to store the total paid in USD in the current month

    # Exchange rates for currencies
    currency_rates = {
        'NGN 🇳🇬': 0.000712758,
        'GHS 🇬🇭': 0.0811322, 
        'GBP 🇬🇧': 1.25401,
        'EUR 🇪🇺': 1.07450,
        'USD 🇺🇸': 1.00000,
    }

    # List of months
    months = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]

    # Create or update the monthly_activity list of dictionaries
    monthly_activity = []

    # Iterate through invoices to find those paid in each month
    for current_month in range(1, 13):
        total_paid_in_current_month_usd = 0  # Initialize a variable to store the total paid in USD in the current month

        for invoice in invoices:
            if invoice.paid_date and invoice.paid_date.month == current_month:
                currency = invoice.currency
                total_paid_in_current_month_usd += invoice.total * currency_rates.get(currency, 0)

        current_month_name = months[current_month - 1]

        # Check if there is an entry for the current month
        current_month_entry = next((entry for entry in monthly_activity if entry['month'] == current_month_name), None)

        if current_month_entry:
            # Update the existing entry for the current month
            current_month_entry['amount'] += total_paid_in_current_month_usd
        else:
            # Create a new entry for the current month
            monthly_activity.append({'month': current_month_name, 'amount': total_paid_in_current_month_usd})

    # Now, monthly_activity will contain a list of dictionaries, each representing a month and its corresponding total amount paid in USD.

    # Calculate currency totals for paid and pending invoices
    paid_total_usd, pending_total_usd = calculate_currency_totals(invoices)

    current_month_num = datetime.now().month

    # 
    context = {
        'clients_num': clients_num, 'invoices_num': invoices_num, 
        'paid_total_usd': paid_total_usd, 'pending_total_usd': pending_total_usd, 'clients': clients,
        'monthly_activity': monthly_activity, 'num': current_month_num
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

    
    # default client image url
    default_clientImg = "https://swift-bill-bucket.s3.amazonaws.com/emil-kowalski.png" 

    context = {'form': form, 'clients': clients, 'clientImg': default_clientImg}
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
    invoices = profile.acc_user.select_related('account_owner').all()
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

            # Check if the invoice is paid, and update the payment_date
            if invoice.invoice_status == 'Paid':
                invoice.paid_date = datetime.now().date()
                invoice.save()

            messages.success(request, 'Invoice created! Click [view invoice] to add items and calculate amount.📝')
            return redirect('invoice')
        else:
            messages.error(request, 'Invalid form: Please check and resubmit')
        
    # default client image url
    default_clientImg = "https://swift-bill-bucket.s3.amazonaws.com/emil-kowalski.png" 

    context = {'form': form, 'invoices': invoices,
               'custom_range': custom_range, 'clientImg': default_clientImg}
    return render(request, 'invoice/invoice.html', context)


########################################## edit-invoice page views
@login_required(login_url='login')
def edit_invoice(request, pk):
    profile = request.user.profile
    # Use get_object_or_404 to handle the case where the invoice does not exist
    invoice = get_object_or_404(profile.acc_user, id=pk)
    
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
        
    # default invoice image url
    default_invoiceImg = "https://swift-bill-bucket.s3.amazonaws.com/invoice.png"

    #
    context = {
        'form': form,
        'invoice': invoice, 
        'display_items': display_items,
        'items_total': items_total,
        'invoiceImg': default_invoiceImg,
    }
    return render(request, 'invoice/invoice-details.html', context)


########################################## preview-invoice page views
@login_required(login_url='login')
def download_invoice(request, pk):
    profile = request.user.profile
    invoice = profile.invoice_set.get(id=pk)

    items = invoice.items.all()
    items_total = invoice.items.aggregate(total=Sum('total'))['total']

    context = {'invoice': invoice, 'profile': profile, 'items': items, 
               'items_total': items_total}

    # Render HTML content
    html_content = render_to_string('invoice/preview-invoice.html', context)

    # Create a PDF file using WeasyPrint
    pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()

    # Create a response with the PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    
    # Set the filename for the download as "invoice.pdf"
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response
