from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, login, hashers

from FeaturesApp.dummyData import dummyDashboardOrdersData, statusColors
from FeaturesApp.models import DeliveryPartner
from .dummyData import dummy_delivery_partner_data

# Create your views here.
def DeliveryLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = DeliveryPartner.objects.filter(email=email).first()
        if user is None:
            messages.error(request, 'Entered Email is not Registered..')
            return redirect('DeliveryPartnerLogin')
        if hashers.check_password(password, user.password) :
            # login(user)
            messages.success(request, 'User has been Logged In')
            return redirect('DeliveryDashboard') 
        
        messages.error(request, 'Entered Password is wrong.')
        return redirect('DeliveryPartnerLogin')
    return render(request, 'delivery/DeliveryLogin.html')

def DeliveryLogout(request):
    logout(request.user)
    messages.warning(request, 'Your has been Logged Out!')
    return render(request, 'delivery/DeliveryLogin.html')


def DeliveryDashboard(request):
    orders = dummyDashboardOrdersData()

    # tab acitve or completed
    tab = request.GET.get('tab','')
    if tab:
        request.session['deliveryPartnerTab'] = tab
    else:
        tab = request.session.get('deliveryPartnerTab', 'active') 

    tracking = request.GET.get("tracking")
    if tracking is not None:
        tracking = tracking == "1"
        request.session["deliveryPartnerTracking"] = tracking
    else:
        tracking = request.session.get("deliveryPartnerTracking", False)

    # handleUpdateStatus(orderid, status) remaining
    orderStatusColors = statusColors()

    otpModal = request.GET.get("otpModal",'')
    if otpModal:
        if otpModal == 'None':
            request.session['deliveryPartnerOtpModal'] = None
            otpModal = None
        else:
            request.session['deliveryPartnerOtpModal'] = otpModal
    else:
        otpModel = request.session.get('deliveryPartnerOtpModal')
    
    # print(f'otpModal = {otpModal}')
    otp = ''

    submitting = False

    cancelModal = request.GET.get("cancelModal",'')
    if cancelModal:
        if cancelModal == 'None':
            request.session['deliveryPartnerCancelModal'] = None
            cancelModal = None
        else:
            request.session['deliveryPartnerCancelModal'] = cancelModal
    else:
        cancelModel = request.session.get('deliveryPartnerCancelModal')
    cancelReason = None

    context={
        'partner':dummy_delivery_partner_data()[0],
        'tab': tab,
        'tracking': tracking,
        'orders':orders,
        'statusColors':orderStatusColors,
        'otpModal':otpModal,
        'otp':otp,
        'cancelModal':cancelModal,
    }
    return render(request, 'delivery/DeliveryDashboard.html', context=context)

def VerifyOtp(request, id):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp:
            print(f'Given OTP for Order id={id} is {otp}')
        else:
            messages.error(request, 'Please enter OTP given by Customer')

    return redirect(request, 'DeliveryDashboard')