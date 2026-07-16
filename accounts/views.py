from django.shortcuts import render, redirect

# Create your views here.
def login_view(request):
    context = {
        "is_login" : True,
    }
    return render(request, "accounts/login.html", context=context)

def register_view(request):
    context = {
        "is_login" : False,
    }
    return render(request, "accounts/login.html", context = context)

def logout_view(request):
    return redirect("Home")