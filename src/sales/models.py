from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone
from django.http import HttpResponse
from .utils import get_code
# Create your models here.


class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        return super().save(*args, **kwargs)
    def __str__(self):
        return f"id: {self.product.id} Product: {self.product.name}"

class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.IntegerField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("sales:detail", kwargs={"pk": self.pk})
    
    

    def __str__(self):
        return str(self.transaction_id[:12])

    def save(self, *args, **kwargs):
        if self.transaction_id == '':
            self.transaction_id = get_code()
        if self.created == None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()


class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csv', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)