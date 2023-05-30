from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from store.models import items
from django.views.generic import DetailView

def item_detail(request:HttpRequest, item_id:int):
    view_item = items.Item.objects.get(pk=item_id)
    context = {"item": view_item}
    return render(request, 'store/item_detail.html', context=context)