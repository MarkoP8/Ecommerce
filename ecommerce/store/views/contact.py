from django.shortcuts import render


# Create your views here.


def contact(request):
    context = {}
    return render(request, 'store/contact.html', context)

def return_item(request):
    context = {}
    return render(request, 'store/return_item.html', context)