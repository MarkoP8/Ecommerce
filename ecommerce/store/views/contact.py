from django.shortcuts import render


# Create your views here.


def contact(request):
    context = {}
    return render(request, 'store/contact.html', context)