from multiprocessing import context

from django.shortcuts import render

# Create your views here.
def Home(request):
    context = {
        "user" : {
            "name" : "John Doe", "email" : "john@example.com", "isAdmin" : True
        },
        "cartCount":12,
        "categoriesData" : [
            { "slug": "fruits-vegetables", "name": "Fruits & Vegetables", "image": "fruits_vegetables" },
            { "slug": "personal-care", "name": "Personal Care", "image": "personal_care" },
            { "slug": "pantry-staples", "name": "Pantry Staples", "image": "pantry_staples" },
            { "slug": "bakery", "name": "Bakery", "image": "bakery" },
            { "slug": "beverages", "name": "Beverages", "image": "drinks" },
            { "slug": "meat-seafood", "name": "Meat & Seafood", "image": "meat_seafood" },
            { "slug": "snacks", "name": "Snacks", "image": "snacks" },
            { "slug": "frozen-foods", "name": "Frozen Foods", "image": "frozen_foods" },
            { "slug": "baby-care", "name": "Baby Care", "image": "baby_care" },
            { "slug": "dairy-eggs", "name": "Dairy & Eggs", "image": "dairy_eggs" },
        ],
    }
    return render(request, "Home.html", context=context)

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