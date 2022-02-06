from django.db import models
from profiles.models import Profile
from django.urls import reverse
# Create your models here.

class Report(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to = 'charts', blank=True, null=True)
    remarks = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse("reports:detail", kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.name)+"---"+str(self.created)