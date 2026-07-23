from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages

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
    return redirect(request.META.get("HTTP_REFERER", "Home"))

def remove_from_cart(request, product_id):
    cart = request.session.get('cart',{})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect(request.META.get("HTTP_REFERER", "Home"))

def update_cart(request, product_id):

    if request.method == "POST":

        action = request.POST.get("action")

        cart = request.session.get("cart", {})

        product_id = str(product_id)

        if product_id in cart:

            if action == "increase":
                cart[product_id] += 1

            elif action == "decrease":
                cart[product_id] -= 1

                if cart[product_id] <= 0:
                    del cart[product_id]
        
        request.session["cart"] = cart

    return redirect(request.META.get("HTTP_REFERER", "Home"))

def clear_cart(request):
    request.session['cart'] = {}
    return redirect(request.META.get("HTTP_REFERER", "Home"))



def Products(request):
    category = request.GET.get("category", "")
    organic = request.GET.get("organic", "")
    sort = request.GET.get("sort", "")
    min_price = request.GET.get("minPrice", "")
    max_price = request.GET.get("maxPrice", "")

    products_data = dummyProducts()
    categories = [{'slug':"", 'name':'All Categories'}] + dummyCategoriesData()

    let = []
    if category:
        for item in products_data:
            if item['category'] == category:
                let.append(item)
    else:
        let = products_data
    if organic == 'true':
        products_data = products_data.filter(is_organic=True)
    if min_price:
        products_data = products_data.filter(price__gte=min_price)
    if max_price:
        prodcuts_data = prodcuts_data.filter(price_lte=max_price)

    if sort == "price_asc":
        products_data = products_data.order_by('price')
    elif sort == 'price_desc':
        products_data = products_data.order_by("-price")
    elif sort == 'rating':
        products_data = products_data.order_by("-rating")
    elif sort == "newest":
        products_data = products_data.order_by("-created_at")

    paginator = Paginator(let, 12)

    page_number = request.GET.get("page")

    let = paginator.get_page(page_number)

    context = {
        "cart" : cart(request),
        # 'products': products_data,
        'products': let,
        'category':category, 
        'categories':categories,
        'organic':organic,
        'sort':sort,
        'min_price':min_price,
        'max_price':max_price,
    }
    return render(request, "Products.html", context=context)

def ProductPage(request,pdid):
    products = dummyProducts()
    product = {}
    for pd in products:
        if pd['id'] == pdid:
            product = pd
            break

    if not product:
        messages.error(request, f"Product with Product Id = {pdid} is not present in data base")
        return redirect(request.META.get("HTTP_REFERER", "Products"))
    
    relatedProducts = []
    for pd in products:
        if pd['id'] != pdid:
            relatedProducts.append(pd)
             
    context={
        'pdid': pdid,
        'product':product,
        'relatedProducts':relatedProducts,
    }
    return render(request, "ProductPage.html", context=context)

def SearchResults(request):
    return render(request, "SearchResults.html")

def FlashDeals(request):
    # filter for product.stock > 0
    context={
        'products':dummyProducts(),
    }
    return render(request, "FlashDeals.html", context=context)

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