from django.shortcuts import render
from django.http import HttpRequest
from store.models import items

def store(request: HttpRequest):
    view_items = items.Item.objects.all()
    context = {'items' : view_items}
    return render(request, 'store/items_list.html', context)

def filter_list(request):
    if request.method == "GET":
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        products = items.Item.objects.all()
        
        if category:
            products = products.filter(category=category)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        print(products)
        print(category)
        print(min_price)
        print(max_price)
        context = {
            'items': products, # html
            'selected_category': category,
            'min_price': min_price,
            'max_price': max_price
        }
        return render(request, 'store/items_list.html', context)