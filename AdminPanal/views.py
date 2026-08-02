from django.shortcuts import render


# Create your views here.
def AdminDashboard(request):
    context={

    }
    return render(request, 'admin/AdminDahboard.html', context=context)

def AdminProducts(request):
    context={

    }
    return render(request, 'admin/AdminProducts.html', context=context)

def AdminProductForm(request):
    context={

    }
    return render(request, 'admin/AdminProductForm.htlm', context=context)

def AdminOrders(request):
    context={

    }
    return render(request, 'admin/AdminOrders.html', context=context)

def AdminDeliveryPartners(request):
    context={

    }
    return render(request, 'admin/AdminDeliveryPartners.html', context=context)