from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models.order import Order
from store.models.order_item import OrderItem 
from store.models.user import User
from store.models.items import Item
from django.contrib import messages
import json


def api_get_number_of_products_in_cart(request):
    user_id = request.user.id
        # Retrieve active orders for the current user
    active_orders = Order.objects.filter(user_id=user_id, ordered=False)
        # Sum up the quantities of all order items in the active orders
    total_items = sum(order_item.quantity for order in active_orders for order_item in order.order_items.all())
    
    return JsonResponse({"num_products": total_items})

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


@login_required(login_url='/login/')
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            itemId = data['itemId']
            action = data['action']
            size_id = data['size_id']
            
            print("Size", size_id)
            #selected_size = request.POST.get('size')
            
            print('ItemId: ', itemId)
            print('Action: ', action)
            #print('Selected size: ', selected_size)
            
            user = request.user
            order, create = Order.objects.get_or_create(user=user, ordered=False)
            
            if action == 'add':
                item = Item.objects.get(id=itemId)
                order_item, created = OrderItem.objects.get_or_create(order=order, item=item, selected_size_id=int(size_id))
                if created:
                    order_item.quantity = 1
                else:
                    order_item.quantity += 1
                order_item.save()
            elif action == 'remove':
                order_item = OrderItem.objects.get(order=order, id=itemId)
                print(order_item.quantity)
                order_item.quantity -= 1
                print(order_item.quantity)
                if order_item.quantity <= 0:
                    order_item.delete()
                else:
                    order_item.save()
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)
            
            return JsonResponse({'success': 'Operation successful'}, status=200)
            
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



def remove_all_items(request):
        if request.method == "POST":
            try:
                user_id = User.objects.get(email=request.user.email)
                order = Order.objects.get(user=user_id, ordered=False)
                order_items = OrderItem.objects.filter(order=order)
                order_items.delete()
                order.delete()
                print("---------------------")
                request.session['success'] = "All items successfully removed from the cart."
            except Exception as e:
                request.session['error'] = "Something went wrong..."
        return redirect('store:home')