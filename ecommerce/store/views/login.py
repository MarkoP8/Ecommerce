from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from django.http import HttpRequest
from store.models import user

def authenticate_user(self, request, email=None, password=None):
        try:
            user_authentication = user.User.objects.get(email=email)
            if user_authentication.check_password(password):
                return user
        except user.User.DoesNotExist:
            return None

def login_user(request: HttpRequest):
    if request.method == "GET":
        error = request.session.get("error", None)
        if error is not None:
            del request.session['error']
        context = {'error': error}
        return render(request, 'store/login.html', context)
    
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        get_user = user.User.objects.get(name=name) # name je zamenjeno umesto email
        if get_user.verify_password(password):
            user_login = authenticate(request, username=name, password=password)
            if user_login is not None:
                login(request, user_login)
                request.session['user'] = get_user.to_dict()
                return redirect('store:home')
        request.session['error'] = "Email and/or password are invalid."
        return redirect('store:login')

def logout_user(request):
    logout(request)
    return redirect('store:home')