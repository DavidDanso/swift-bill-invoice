from django import forms
from django.forms import ModelForm
from .models import *


# Client Creation form
class ClientCreationForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'address', 'country', 'city_state', 'email', 'phone_number', 'postal_code', 'client_avatar']
        # add id and placeholder to the input field
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '...'}),
            'address': forms.TextInput(attrs={'placeholder': '...'}),
            'country': forms.TextInput(attrs={'placeholder': '...'}),
            'city_state': forms.TextInput(attrs={'placeholder': '...'}),
            'email': forms.TextInput(attrs={'placeholder': '...'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '...'}),
            'postal_code': forms.TextInput(attrs={'placeholder': '...'}),
        }
    # add class to the input field
    def __init__(self, *args, **kwargs):
        super(ClientCreationForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class': 'input form-control'})


class DateInput(forms.DateInput):
    input_type = 'date'

# Invoice Creation form
class InvoiceCreationForm(ModelForm):
    payment_date = forms.DateField(widget=DateInput)
    class Meta:
        model = Invoice
        fields = ['project_name', 'project_duration', 'client_name', 
                  'invoice_status', 'payment_date', 'currency', 
                  'item_title', 'quantity', 'price', 'client_note']

    def __init__(self, user, *args, **kwargs):
        super(InvoiceCreationForm, self).__init__(*args, **kwargs)

        # Set default value for the invoice_status field
        self.fields['invoice_status'].widget.choices = [('', 'Choose status')] + list(self.fields['invoice_status'].widget.choices)

        # Set default value for the currency field
        self.fields['currency'].widget.choices = [('', 'Choose currency')] + list(self.fields['currency'].widget.choices)

        # Filter clients based on the current user
        self.fields['client_name'].queryset = Client.objects.filter(account_owner=user.profile)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input form-control'})

    

