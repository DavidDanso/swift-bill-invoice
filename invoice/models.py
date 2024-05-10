from django.db import models
from user.models import Profile
import uuid
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_resized import ResizedImageField
# import requests


# client model   
class Client(models.Model):
    account_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='clients', db_index=True)
    name = models.CharField(max_length=50, unique=True, db_index=True)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    phone_number = models.IntegerField(null=True, blank=True)
    city_state = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=30, null=True, blank=True)
    client_avatar = ResizedImageField(size=[600, 600], quality=85, null=True, blank=True, upload_to='client_avatar/', default='emil-kowalski.png')
    updated_time_stamp = models.DateTimeField(auto_now=True, db_index=True)
    created_time_stamp = models.DateTimeField(auto_now_add=True, db_index=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    @property
    def imageURL(self):
        try:
            url = self.client_avatar.url
        except:
            url = ''
        return url
    
    @property
    def first_name(self):
        return self.name.split()[0] if self.name else ''
    
    # display new clients first
    class Meta:
        ordering = ['-updated_time_stamp']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['updated_time_stamp']),
            models.Index(fields=['created_time_stamp']),
        ]
    
    # display client with names in the database
    def __str__(self):
        return self.name
    

# invoice model   
class Invoice(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    )

    CURRENCY = (
        ('USD 🇺🇸', 'USD 🇺🇸'),
        ('GHS 🇬🇭', 'GHS 🇬🇭'),
        ('GBP 🇬🇧', 'GBP 🇬🇧'),
        ('EUR 🇪🇺', 'EUR 🇪🇺'),
        ('NGN 🇳🇬', 'NGN 🇳🇬'),
    )

    account_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='acc_user', db_index=True)
    project_name = models.CharField(max_length=255)
    project_duration = models.CharField(max_length=50)
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE, to_field='name', related_name='invoice', db_index=True, 
                                    help_text='Select a client for this entry.')
    invoice_status = models.CharField(max_length=200, choices=STATUS, db_index=True)
    payment_date = models.DateField(max_length=200, null=True)
    currency = models.CharField(max_length=200, choices=CURRENCY)
    invoice_image = ResizedImageField(size=[600, 600], quality=85, null=True, blank=True, upload_to='invoice_image/', default='invoice.png')
    client_note = models.TextField(max_length=100000, null=True, blank=True)

    total = models.IntegerField(default=0, null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)

    updated_time_stamp = models.DateTimeField(auto_now=True, db_index=True)
    created_time_stamp = models.DateTimeField(auto_now_add=True, db_index=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    
    @property
    def invoiceImageURL(self):
        try:
            url = self.invoice_image.url
        except:
            url = ''
        return url
    
    # display new invoice first
    class Meta:
        ordering = ['-updated_time_stamp']
    
    # display invoice with project_names in the database
    def __str__(self):
        return self.project_name
    

class Item(models.Model):
    account_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, related_name='items')
    title = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    total = models.IntegerField(default=0, null=True, blank=True)
    updated_time_stamp = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    @property
    def invoice_total(self):
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        # Convert quantity, price, and invoice_total to integers before saving
        self.quantity = int(self.quantity)
        self.price = int(self.price)
        self.total = int(self.invoice_total)

        super(Item, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_time_stamp']

    
    def __str__(self):
        return f'{self.invoice.project_name} : {self.title}'
    

@receiver(post_save, sender=Item)
def update_invoice_total_on_item_change(sender, instance, **kwargs):
    """
    Signal handler to update the corresponding Invoice total
    when a new Item is created or an existing Item is updated.
    """
    update_invoice_total(instance.invoice)

@receiver(post_delete, sender=Item)
def update_invoice_total_on_item_delete(sender, instance, **kwargs):
    """
    Signal handler to update the corresponding Invoice total
    when an Item is deleted.
    """
    update_invoice_total(instance.invoice)

def update_invoice_total(invoice):
    """
    Helper function to update the total of an Invoice based on its items.
    """
    if invoice:
        items = invoice.items.all()
        invoice.total = sum(item.total for item in items)
        invoice.save()


