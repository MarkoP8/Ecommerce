from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.http import HttpRequest
from store.models import user
from store.authentication.custom_auth import EmailAuthBackend

'''def authenticate_user(request, email=None, password=None):
    try:
        user_authentication = user.User.objects.get(email=email)
        if user_authentication.verify_password(password):
            return user_authentication
    except user.User.DoesNotExist:
        return None'''

def login_user(request: HttpRequest):
    if request.method == "GET":
        error = request.session.get("error")
        if error:
            del request.session['error']
        context = {'error': error}
        return render(request, 'store/login.html', context)
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Attempting to log in with email: {email} and {password}") 

        try:
            user_obj = user.User.objects.get(email=email)
            print("User found in the database:", user_obj)

            if user_obj.verify_password(password):
                print("Password verified successfully")
                user_login = authenticate(request, email=email, password=password)
                if user_login is not None:
                    print("User authenticated successfully")
                    login(request, user_login)
                    request.session['user'] = user_obj.to_dict()
                    return redirect('store:home')
                else:
                    print("Authentication failed: Invalid email or password")
                    request.session['error'] = "Invalid email or password"
            else:
                print("Password verification failed")
                request.session['error'] = "Invalid email or password"
        except user.User.DoesNotExist:
            print("User not found")
            request.session['error'] = "User not found"

        return redirect('store:login')

def logout_user(request):
    logout(request)
    return redirect('store:home')
