from django.db import models


# Create your models here.
class Dataset(models.Model):
    name = models.CharField(max_length=200, null=True)
    age = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    pic = models.ImageField(default="profile.png", null=True, blank=True)

    def __str__(self):
        return self.name