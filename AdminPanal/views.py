from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from httpx import RequestError

from AdminPanal.dummyData import dummy_admin_dashboard_data
from DeliveryPartner.dummyData import dummy_delivery_partner_data
from FeaturesApp.dummyData import dummyCategoriesData, dummyDashboardOrdersData, dummyProducts
from FeaturesApp.models import Product

from .forms import AdminProductForms


# Create your views here.
AdminLinkData = [
    { 'to': "AdminDashboard", 'label': "Dashboard", 'icon': 'bar-chart-3' },
    { 'to': "AdminProductForm", 'label': "Add Product", 'icon': 'plus' },
    { 'to': "AdminProducts", 'label': "Products", 'icon': 'package-search' },
    { 'to': "AdminOrders", 'label': "Orders", 'icon': 'shopping-bag' },
    { 'to': "AdminDeliveryPartners", 'label': "Delivery Partners", 'icon': 'truck' },
    { 'to': "AdminLogout", 'label': "Exit", 'icon': 'log-out' },
]

def AdminLogout(request):
    return redirect('Login')

def AdminDashboard(request):

    stats = dummy_admin_dashboard_data()
    card = []
    if stats:
        cards = [
            { 'label': "Total Orders", 'value': stats['totalOrders'], 'icon': 'shopping-bag' },
            { 'label': "Total Users", 'value': stats['totalUsers'], 'icon': 'users' },
            { 'label': "Total Products", 'value': stats['totalProducts'], 'icon': 'package' },
            { 'label': "Out of Stock", 'value': stats['outOfStock'], 'icon': 'alert-triangle' },
        ]

    context={
        'AdminLinkData':AdminLinkData,
        'stats':stats,
        'cards':cards,
    }
    return render(request, 'admin/AdminDashboard.html', context=context)

def AdminProducts(request):

    products = dummyProducts()
    productId = request.GET.get('productId','')
    if productId:
        messages.warning(request,f'Product #{productId[-6:].upper()} is set for stock out')

    context={
        'AdminLinkData':AdminLinkData,
        'products':products,
    }
    return render(request, 'admin/AdminProducts.html', context=context)

def AdminProductForm(request, id=None):
    product=None

    if id:
        product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        form = AdminProductForms(request.POST, request.FILES, instance=Product,)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product saved successfully')
            return redirect('AdminProducts')
    else:
        form = AdminProductForms(instance=product)

    context={
        'AdminLinkData':AdminLinkData,
        'isEdit':product is not None,
        'categoriesData':dummyCategoriesData(),
        'form':form,
        'product':product,
    }
    return render(request, 'admin/AdminProductForm.html', context=context)

def AdminOrders(request):
    orders = dummyDashboardOrdersData()
    partners = dummy_delivery_partner_data()
    statusOptions = ["Placed", "Confirmed", "Assigned", "Packed", "Out for Delivery", "Delivered", "Cancelled"]

    selectedPartner = ''
    if request.method == 'POST':
        if 'assignPartner' in request.POST:
            selectedPartner = request.POST.get('partner')
    
        if selectedPartner:
            assignModal = request.session.get('assignModal')
            messages.success(request, f"Order #{assignModal[-6:].upper()} has been assigned to #{selectedPartner[-6:].upper()} successfully.")

    assignModal = request.GET.get('assignModal')
    if assignModal :
        if assignModal == 'None':
            request.session['assignModal'] = None
            assignModal = None
        else:
            request.session['assignModal'] = assignModal
            selectedPartner = ''
    else:
        assignModal = request.session.get('assignModal')
    
    
    context={
        'AdminLinkData':AdminLinkData,
        'orders':orders,
        'partners':partners,
        'statusOptions':statusOptions,
        'assignModal':assignModal,
        'selectedPartner':selectedPartner,

    }
    return render(request, 'admin/AdminOrders.html', context=context)

def AdminDeliveryPartners(request):

    partners = dummy_delivery_partner_data()

    context={
        'AdminLinkData':AdminLinkData,
        'partners':partners,
    }
    return render(request, 'admin/AdminDeliveryPartners.html', context=context)