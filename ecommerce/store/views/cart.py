from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models.order import Order
from store.models.order_item import OrderItem 
from store.models.user import User
from store.models.items import Item 
import json

@login_required(login_url='/login/')
def view_cart(request):
    total_price = 0
    items = []
    error = ""
    if request.user.is_authenticated:
            user_id = User.objects.get(email=request.user.email)
            orders = Order.objects.filter(user=user_id, ordered=False)
            for order in orders:
                order_items = order.order_items.all() # order_items zbog related_name in order item
                for item in order_items:
                    if item.item.dicount_price:
                        item.quantity_price = item.item.dicount_price * item.quantity
                    else:
                        item.quantity_price = item.item.price * item.quantity
                    total_price += item.quantity_price
                    items.append(item)
    else:
        error = "Something went wrong..."
    
    context = {'items': items, 'total_price': total_price, 'error': error}
    return render(request, 'store/cart.html', context)



def add_to_cart(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        itemId = data['itemId']
        action = data['action']
        
        print('ItemId: ', itemId)
        print('Action: ', action)
        user = User.objects.get(name=request.user.username)
        item = Item.objects.get(id=itemId)
        order, create = Order.objects.get_or_create(user=user, ordered=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        if created:
            order_item.quantity = 1
        else:
            if action == 'add':
                order_item.quantity += 1
            elif action == 'remove':
                order_item.quantity -= 1
                print(order_item.quantity, "**************************")
            order_item.save()
            if order_item.quantity <= 0:
                order_item.delete()
            order_item.save()
    except json.JSONDecodeError as e:
        print('Error decoding JSON:', str(e))
        return JsonResponse('Invalid JSON payload', status=400, safe=False)
    except KeyError as e:
        print('Missing key in JSON:', str(e))
        return JsonResponse('Missing key in JSON payload', status=400, safe=False)
    
    return JsonResponse('Cart is updated...', safe=False)

def remove_all_items(request):
        if request.method == "POST":
            try:
                user_id = User.objects.get(name=request.user.username)
                order = Order.objects.get(user=user_id, ordered=False)
                order_items = OrderItem.objects.filter(order=order)
                print("------------------1", order_items)
                order_items.delete()
                print(order_items, "//////////////////////////")
                print(order, "****************************")
                order.delete()
                print(order)
                
                request.session['success'] = "All items successfully removed from the cart."
                return redirect('store:cart')
            except Exception as e:
                print(str(e))
                request.session['error'] = "Something went wrong..."
                return redirect('store:cart')
        print("-------------------------------------------------------------")
        return redirect('store:cart')