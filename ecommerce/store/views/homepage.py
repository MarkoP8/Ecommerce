from django.shortcuts import render
from store.models.order import Order


def home(request):
    success = request.session.get('success', None)
    error = request.session.get('error', None)
    if success is not None:
        del request.session['success']
    if error is not None:
        del request.session['error']
    
    total_items = 0
    if request.user.is_authenticated:
        user_id = request.user.id
        # Retrieve active orders for the current user
        active_orders = Order.objects.filter(user_id=user_id, ordered=False)
        # Sum up the quantities of all order items in the active orders
        total_items = sum(order_item.quantity for order in active_orders for order_item in order.order_items.all())
    context = { "success": success , "error": error, 'total_items': total_items}
    return render(request,"store/home.html", context)

def about(request):
    context = {}
    return render(request, "store/about.html", context)