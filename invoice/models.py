from django.db import models
from user.models import Profile
import uuid

# client model   
class Client(models.Model):
    account_owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255, default='...')
    country = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True, default='...')
    phone_number = models.IntegerField(null=True, blank=True, default='(xxx)xxx-xxxx')
    city_state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=30, default='...')
    client_avatar = models.ImageField(null=True, blank=True, upload_to='client_avatar/', default='emil-kowalski.png')
    updated_time_stamp = models.DateTimeField(auto_now=True)
    created_time_stamp = models.DateTimeField(auto_now_add=True)
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
    
    # display clinet with names in the database
    def __str__(self):
        return self.name
    

# invoice model   
class Invoice(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    )

    CURRENCY = (
        ('USD', 'USD'),
        ('GHC', 'GHC'),
        ('GBP', 'GBP'),
        ('EUR', 'EUR'),
    )

    account_owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    project_duration = models.CharField(max_length=50)
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE, to_field='name', related_name='invoice', 
                                    help_text='Select a client for this entry.')
   
    invoice_status = models.CharField(max_length=200, choices=STATUS)
    payment_date = models.DateField(max_length=200, null=True)
    currency = models.CharField(max_length=200, choices=CURRENCY)
    item_title = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    total = models.IntegerField(default=0, null=True, blank=True)
    client_note = models.TextField(max_length=100000, null=True, blank=True)
    updated_time_stamp = models.DateTimeField(auto_now=True)
    created_time_stamp = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    
    @property
    def invoice_total(self):
        return self.quantity * self.price
    
    # Override the save method to update the total before saving
    def save(self, *args, **kwargs):
        self.total = self.invoice_total
        super(Invoice, self).save(*args, **kwargs)
    
    # display new invoice first
    class Meta:
        ordering = ['-updated_time_stamp']
    
    # display invoice with project_names in the database
    def __str__(self):
        return self.project_name
    
