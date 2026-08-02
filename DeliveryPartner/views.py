from django.shortcuts import render
from .dummyData import dummy_delivery_partner_data

# Create your views here.
def DeliveryLogin(request):
    context={

    }
    return render(request, 'delivery/DeliveryLogin.html', context=context)

def DeliveryLogout(request):

    return render(request, 'delivery/DeliveryLogin.html')

def DeliveryDashboard(reqeust):
    context={
        'partner':dummy_delivery_partner_data()[0],
    }
    return render(reqeust, 'delivery/DeliveryDashboard.html', context=context)

