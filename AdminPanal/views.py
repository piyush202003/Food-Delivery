from django.shortcuts import render,redirect

from AdminPanal.dummyData import dummy_admin_dashboard_data


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
    context={
        'AdminLinkData':AdminLinkData,
    }
    return render(request, 'admin/AdminProducts.html', context=context)

def AdminProductForm(request):
    context={
        'AdminLinkData':AdminLinkData,
    }
    return render(request, 'admin/AdminProductForm.html', context=context)

def AdminOrders(request):
    context={
        'AdminLinkData':AdminLinkData,
    }
    return render(request, 'admin/AdminOrders.html', context=context)

def AdminDeliveryPartners(request):
    context={
        'AdminLinkData':AdminLinkData,
    }
    return render(request, 'admin/AdminDeliveryPartners.html', context=context)