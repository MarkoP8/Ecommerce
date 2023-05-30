from django.db import models
from django.utils import timezone
from store.models import items, order

class OrderItem(models.Model):
    item = models.ForeignKey(items.Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(order.Order, related_name='order_items', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity} of {self.item} ({self.order})"