from django.shortcuts import render
from django.contrib.auth import login
from django.db import IntegrityError
from django.http import HttpResponseNotFound
from store.models import user

def register(request):
    if request.method == "GET":
        return render(request, 'store/register.html')
            
    if request.method == "POST":
        new_user = user.User()
        new_user.name = request.POST['name']
        new_user.email  = request.POST['email']
        new_user.create_hashed_password(request.POST['password'])
        try:
            new_user.save()
            login(request, new_user)
            success = 'You have created an acount'
            context = {'success': success}
            return render(request, 'store/home.html', context=context)
        except IntegrityError as ie:
            error = f"User with that {request.POST['email']} alredy exists."
            context = {'error': error}
            return render(request, 'store/login.html', context)
        except Exception as ex:
            return HttpResponseNotFound(f"{ex}")
    else:
        error = "Something went wrong."
        context = {'error': error}
        return render(request, 'store:login', context)