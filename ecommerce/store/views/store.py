from django.shortcuts import render
from django.http import HttpRequest
from store.models import items

def store(request: HttpRequest):
    view_items = items.Item.objects.all()
    context = {'items' : view_items}
    return render(request, 'store/items_list.html', context)