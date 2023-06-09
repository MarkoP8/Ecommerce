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
                    total_price = round(total_price, 2)
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
        order, create = Order.objects.get_or_create(user=user, ordered=False)
        
        if action == 'add':
            item = Item.objects.get(id=itemId)
            order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
            if created:
                order_item.quantity = 1
            else:
                order_item.quantity += 1
            order_item.save()
        
        else:
            if action == 'remove':
                order_item = OrderItem.objects.get(order=order, id=itemId)
                order_item.quantity -= 1
                if order_item.quantity <= 0:
                    order_item.delete()
                else:
                    order_item.save()
        
    except json.JSONDecodeError as e:
        return JsonResponse('Invalid JSON payload', status=400, safe=False)
    except KeyError as e:
        return JsonResponse('Missing key in JSON payload', status=400, safe=False)
    except Item.DoesNotExist as e:
        return JsonResponse('Item matching query does not exist', status=400, safe=False)
    
    return JsonResponse('Cart is updated...', safe=False)


def remove_all_items(request):
        if request.method == "POST":
            try:
                user_id = User.objects.get(name=request.user.username)
                order = Order.objects.get(user=user_id, ordered=False)
                order_items = OrderItem.objects.filter(order=order)
                order_items.delete()
                order.delete()
                
                request.session['success'] = "All items successfully removed from the cart."
                return redirect('store:cart')
            except Exception as e:
                request.session['error'] = "Something went wrong..."
                return redirect('store:cart')
        return redirect('store:cart')