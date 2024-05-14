from django.db import models
from django.conf import settings
from django import forms

# prvo ide u db, drugo je ono sto prikazujemo
CATEGORY_CHOICES = (
    ('Hoodies', 'Hoodies'),
    ('Shorts', 'Shorts'),
    ('T-Shirt', 'T-Shirt')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, blank=True, null=True)
    dicount_price = models.FloatField(default=None, null=True, blank=True)
    sizes = models.ManyToManyField('ItemSize', related_name='items')
    images = models.ManyToManyField('ItemImage', related_name='items')
    
    def __str__(self):
        return self.title
    
    def image_url(self):
        return f"{settings.STATIC_URL}{self.image}"
    
class ItemImage(models.Model):
    image = models.ImageField(upload_to='store/static/images/')

    def __str__(self):
        return self.image.url

class ItemSize(models.Model):
    size = models.CharField(max_length=4, null=True)
    
    def __str__(self) -> str:
        return self.size