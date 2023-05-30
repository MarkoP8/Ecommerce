from django.db import models
from django.conf import settings

# prvo ide u db, drugo je ono sto prikazujemo
"""CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danegr')
)"""


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    #category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, default=None, null=True)
    #label = models.CharField(choices=LABEL_CHOICES, max_length=1, default=None, null=True, blank=True)
    dicount_price = models.FloatField(default=None, null=True, blank=True)
    image = models.ImageField(default=None, upload_to='store/static/images/')
    
    def __str__(self):
        return self.title
    
    def image_url(self):
        return f"{settings.STATIC_URL}{self.image}"