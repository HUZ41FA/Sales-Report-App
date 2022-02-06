from django.db import models
from django.http import HttpResponse

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='customers', default = 'no-picture.png')

    def __str__(self):
        return str(self.name)