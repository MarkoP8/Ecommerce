from django.db import models
from django.utils import timezone
from store.models import items, order

class OrderItem(models.Model):
    item = models.ForeignKey(items.Item, on_delete=models.SET_NULL, null=True)
    selected_size = models.ForeignKey('ItemSize', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(order.Order, related_name='order_items', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.selected_size:
            return f"{self.quantity} {self.item} - {self.selected_size.size} ({self.order})"
        else:
            return f"{self.quantity} {self.item} - No size selected ({self.order})"