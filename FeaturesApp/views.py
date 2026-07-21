from multiprocessing import context

from django.shortcuts import render, redirect, get_object_or_404
from .dummyData import dummyProducts, dummyCategoriesData
from .models import Product

# Create your views here.
def Home(request):
    context = {
        "cartCount":12,
        "categoriesData" : dummyCategoriesData(),
        "products" : dummyProducts(),
        "cart" : cart(request)
    }
    return render(request, "Home.html", context=context)

def cart(request):
    cart = request.session.get("cart", {})
    cart_items = []
    cart_total = 0
    cart_count = 0
    for product_id, quantity in cart.items():
        # product = get_object_or_404(Product, id=product_id)
        for item in dummyProducts():
            if item["id"] == product_id:
                product = item
        # total_price = product.price * quantity
        if product:
            total_price = product['price'] * quantity
            cart_items.append({
                "product":product,
                "quantity":quantity,
                "total":total_price,
            })
            cart_total += total_price
            cart_count += 1
    
    delivery_fee = 0
    if cart_total <= 20:
        delivery_fee = 1.99

    context = {
        "cart_items":cart_items,
        "cart_total":cart_total,
        "cart_count":cart_count,
        "grand_total": cart_total + delivery_fee,
        "delivery_fee":delivery_fee,
    }

    return context

def add_to_cart(request, product_id):
    for item in dummyProducts():
        if item["id"] == product_id:
            product = item
    cart = request.session.get("cart",{})
    
    product_id = str(product_id)
    
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart
    return redirect("Home")

def remove_from_cart(request, product_id):
    cart = request.session.get('cart',{})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect("Home")

def update_cart(request, product_id):

    if request.method == "POST":

        action = request.POST.get("action")

        cart = request.session.get("cart", {})

        product_id = str(product_id)
        print("before adding = ", cart[product_id])

        if product_id in cart:

            if action == "increase":
                cart[product_id] += 1

            elif action == "decrease":
                cart[product_id] -= 1

                if cart[product_id] <= 0:
                    del cart[product_id]
        
        print("after adding = ", cart[product_id])
        request.session["cart"] = cart

    return redirect("Home")

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('Home')



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
    context = {
        "cart":cart(request),
    }
    return render(request, "Checkout.html", context=context)

def MyOrders(request):
    return render(request, "MyOrders.html")

def OrderTracking(request, odid):
    return render(request, "OrderTracking.html", {"odid" : odid})

def Addresses(request):
    return render(request, "Addresses.html")