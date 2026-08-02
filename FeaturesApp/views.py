from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages

from .dummyData import dummyProducts, dummyCategoriesData, generate_dummy_reviews, get_rating_breakdown, dummyDashboardOrdersData, statusColors, dummyAddressData
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
        if pd['id'] != pdid and pd['category'] == product['category']:
            relatedProducts.append(pd)

    cartData = request.session.get("cart",{})
    # product_id = str(product.id)
    displayQuantity = cartData.get(pdid, 0)
    inCart = pdid in cartData
    categoryLabel = product['category'].replace("-", " ")

    reviews = generate_dummy_reviews(product)
    breakdown = get_rating_breakdown(reviews)

    context={
        'pdid': pdid,
        'product':product,
        'relatedProducts':relatedProducts,
        'cart': cart(request),
        'displayQuantity': displayQuantity,
        'inCart': inCart,
        'categoryLabel': categoryLabel,
        'reviews':reviews,
        'breakdown':breakdown,
        'maxRatingCount':max(breakdown),
    }
    return render(request, "ProductPage.html", context=context)

def SearchResults(request):
    cartData = cart(request)

    search = request.GET.get('search','')

    products = dummyProducts()
    resultProducts = []
    for product in products:
        if search in product['name'].lower():
            resultProducts.append(product)

    context = {
        'search':search,
        'products': resultProducts,
        'cart': cartData,
    }
    return render(request, "SearchResults.html", context=context)

def FlashDeals(request):
    # filter for product.stock > 0
    context={
        'products':dummyProducts(),
    }
    return render(request, "FlashDeals.html", context=context)

# from here all are needed authentication verification
def Checkout(request):
    cartData = cart(request)

    user = {
        'addresses':dummyAddressData(),
    }
    address = {
        'id':'',
        'label':'Home',
        'address':'',
        'city':'',
        'state':'',
        'zip':'',
        'isDefault':False,
        'lat':0,
        'lng':0
    }

    newAdd = request.GET.get('addrId','')
    prevAdd = request.session.get('addrId','')
    for add in user['addresses']:
        if newAdd:
            if add['id'] == newAdd:
                address = add
                request.session['addrId'] = add['id']
                break
        elif prevAdd:
            if add['id'] == prevAdd:
                address = add
                request.session['addrId'] = add['id']
                break
        else:
            if add['isDefault']:
                address = add
                request.session['addrId'] = add['id']
                break
    address = request.GET.get('address', address)

    paymentMethod = request.session.get("paymentMethod", "cash")

    if request.method == "POST":
        paymentMethod = request.POST.get("payment_method")

        request.session["paymentMethod"] = paymentMethod


    deliveryFee = 0
    if cartData['cart_total'] <= 20:
        deliveryFee = 1.99
    tax = cartData['cart_total'] * 0.08
    total = cartData['cart_total'] + deliveryFee + tax

    step = request.GET.get("step", "address")
    steps = [
        {'key':'address', 'label':'Address', 'icon':'map-pin'},
        {'key':'payment', 'label':'Payment', 'icon':'credit-card'},
        {'key':'review', 'label':'Review', 'icon':'check'},
    ]
    

    context = {
        "cart":cartData,
        'user':user,
        'address':address,
        'paymentMethod':paymentMethod,
        'deliveryFee':deliveryFee,
        'tax':tax,
        'total':total,
        'step':step,
        'steps':steps,
    }
    return render(request, "Checkout.html", context=context)

def MyOrders(request):

    activeTab = request.GET.get('activeTab','All Orders')
    orders = dummyDashboardOrdersData()
    statusCol = statusColors()
    # print(statusCol)
    for order in orders:
        order['statusColour'] = statusCol[order['status']]
        order['itemsExtraCount'] = len(order['items']) - 4

    context={
        'cart':cart(request),
        'orders':orders,
        'tabs':['All Orders', 'Placed', 'Out For Delivery', 'Delivered'],
        'activeTab':activeTab,
        'statusColours':statusColors(),

    }
    return render(request, "MyOrders.html", context=context)

def OrderTracking(request, odid):
    order = {}
    allStatus = ['Placed', 'Confirmed', 'Assigned', 'Packed', 'Out for Delivery', 'Delivered']
    statusCol = statusColors()
    for od in dummyDashboardOrdersData():
        if od['id'] == odid:
            order = od
            order['statusColour'] = statusCol[order['status']]
            break

    if not order:
        messages.error(request, "There is no order with order id = ", odid)
        return redirect(request.META.get("HTTP_REFERER", "MyOrders"))

    showOtp = order['deliveryOtp'] and order['status'] in allStatus[2:5]

    liveLocation = None
    if order['status'] in allStatus[2:5]:
        liveLocation = order['liveLocation']

    statusIcons = {
        "Placed": "clock",
        "Confirmed": "check",
        "Assigned": "truck",
        "Packed": "package",
        "Out for Delivery": "truck",
        "Delivered": "check",
    }
    statusHistory = {
        history['status']: history['timestamp']
        for history in order['statusHistory']
    }

    def get_timestamp(status):
        for his in order['statusHistory']:
            if his['status'] == status:
                return his['timestamp']

    allStatusInfo = [
        {
            'status':'Placed',
            'icon':'clock',
            'timestamp': get_timestamp('Placed')
        },{
            'status':'Confirmed',
            'icon':'check',
            'timestamp': get_timestamp('Confirmed')
        },{
            'status':'Assigned',
            'icon':'truck',
            'timestamp': get_timestamp('Assigned')
        },{
            'status':'Packed',
            'icon':'package',
            'timestamp': get_timestamp('Packed')
        },{
            'status':'Out for Delivery',
            'icon':'truck',
            'timestamp': get_timestamp('Out for Delivery')
        },{
            'status':'Delivered',
            'icon':'check',
            'timestamp': get_timestamp('Delivered')
        }
    ]

    context={
        "order":order,
        'liveLocation': None,
        'showOtp': showOtp,
        'liveLocation':liveLocation,
        'allStatus':allStatus,
        'statusIcons': statusIcons,
        'currentIdx':allStatus.index(order['status']),
        'statusHistory':statusHistory,
        'allStatusInfo':allStatusInfo,
    }
    return render(request, "OrderTracking.html", context=context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@csrf_exempt  # Remove @csrf_exempt if passing CSRF header/token from app
def update_driver_location(request, odid):
    """
    Endpoint called by driver's mobile app or GPS tracker to push location updates.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = float(data.get("lat"))
            lng = float(data.get("lng"))

            # 1. Broadcast the new location to WebSocket subscribers
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"order_{odid}",
                {
                    "type": "location_update",
                    "lat": lat,
                    "lng": lng,
                }
            )

            # 2. Optionally update your DB / cache here if needed...

            return JsonResponse({"status": "success", "lat": lat, "lng": lng})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "invalid_method"}, status=405)

def Addresses(request):
    context = {
        'addresses': dummyAddressData(),
    }
    return render(request, "Addresses.html", context=context)

def AddressDelete(request, addid):
    addresses = dummyAddressData()

    # Address.objects.filter(id=addid).delete()
    for address in addresses:
        if address['id'] == addid:
            del address['id']
            break
    print(addresses)
    
    return redirect(request.META.get("HTTP_REFERER", "Addresses"))