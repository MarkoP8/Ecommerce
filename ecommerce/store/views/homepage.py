from django.shortcuts import render


def home(request):
    success = request.session.get('success', None)
    error = request.session.get('error', None)
    if success is not None:
        del request.session['success']
    if error is not None:
        del request.session['error']
    context = { "success": success , "error": error}
    return render(request,"store/home.html", context)