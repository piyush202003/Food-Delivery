from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, "Home.html")

def Products(request):
    return render(request, "Products.html")

def ProductPage(request,pdid):
    context = {'pdid': pdid}
    return render(request, "ProductPage.html", {"context":context})

def SearchResults(request):
    return render(request, "SearchResults.html")

def FlashDeals(request):
    return render(request, "FlashDeals.html")

# from here all are needed authentication verification
def Checkout(request):
    return render(request, "Checkout.html")

def MyOrders(request):
    return render(request, "MyOrders.html")

def OrderTracking(request, odid):
    return render(request, "OrderTracking.html", {"odid" : odid})

def Addresses(request):
    return render(request, "Addresses.html")