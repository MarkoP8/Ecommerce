from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user, items, order, order_item, address

# Register your models here.
admin.site.register(user.User)
admin.site.register(order.Order)
admin.site.register(order_item.OrderItem)
admin.site.register(items.Item)
admin.site.register(items.ItemImage)
admin.site.register(items.ItemSize)
admin.site.register(address.Address)