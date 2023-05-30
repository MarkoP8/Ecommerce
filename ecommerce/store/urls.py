from django.urls import path
from .views import homepage, cart, checkout, contact, item_detail, login, register, store

app_name = 'store'
urlpatterns = [
    path('', homepage.home, name='home'),
    path('cart/', cart.view_cart, name='cart'),
    path('add_to_cart/', cart.add_to_cart, name='add_to_cart'),
    path('remove_all_items/', cart.remove_all_items, name='remove_all_items'),
    path('checkout/', checkout.checkout, name='checkout'),
    path('store/', store.store, name='items_list') ,
    path('register/', register.register, name='register'),
    path('login/', login.login_user, name='login'),
    path('logout/', login.logout_user, name='logout'),
    path('contact/', contact.contact, name='contact'),
    path('item-detail/<int:item_id>/', item_detail.item_detail, name='item_detail')
]