from django.shortcuts import render

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