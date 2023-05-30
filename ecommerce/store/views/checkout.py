from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from store.models import user, items, order, order_item, address

@login_required(login_url='/login/')
def checkout(request):
    if request.method == 'GET':
        item_titles = []
        item_price = []
        item_quantity = []
        total_price = 0
        total_items = 0
        
        if request.user.is_authenticated:
            user_id = user.User.objects.get(name=request.user.username)
            cart_order = order.Order.objects.filter(user=user_id, ordered=False).first()
            if cart_order:
                order_items = order_item.OrderItem.objects.filter(order=cart_order)
                for item in order_items:
                    item_titles.append(item.item.title)
                    item_price.append(item.item.price)
                    item_quantity.append(item.quantity)
                    total_price = item.item.price * item.quantity
                    total_items += item.quantity
                context = {'order_items': order_items, 'total_price': total_price, 'total_items': total_items}
                return render(request, 'store/checkout.html', context)
    if request.method == 'POST':
        shipping_address = address.Address()
        shipping_address.name = request.POST['name']
        shipping_address.email = request.POST['email']
        shipping_address.country = request.POST['country']
        shipping_address.city = request.POST['city']
        shipping_address.zip_code = request.POST['zip_code']
        shipping_address.street_address = request.POST['street_address']
        shipping_address.card_name = request.POST['card_name']
        shipping_address.credit_card = request.POST['credit_card']
        shipping_address.exp_month = request.POST['exp_month']
        shipping_address.exp_year = request.POST['exp_year']
        shipping_address.cvv = request.POST['cvv']
        try:
            shipping_address.save()
            if request.user.is_authenticated:
                user_id = user.User.objects.get(name=request.user.username)
                cart_order = order.Order.objects.filter(user=user_id, ordered=False).first()
                if cart_order:
                    cart_order.address = shipping_address
                    cart_order.ordered = True
                    cart_order.save()
            success = 'Data saved successfully'
            context = {'success': success}
            return render(request, 'store/message.html', context)
        except Exception as e:
            return HttpResponse(f"----------{e}")
    else:
        error = "Something went wrong..."
        context = {'error': error}
        return render(request, 'store/checkout.html', context)