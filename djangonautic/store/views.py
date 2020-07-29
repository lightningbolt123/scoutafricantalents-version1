from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Visitor, Item, Entry
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.utils import timezone
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def store_view(request):
    products = Item.objects.all()
    return render(request, 'store/store.html', {'products':products})

def subscribe(request, id):
    item = get_object_or_404(Item, id=id)
    today = timezone.now()
    item_name = item.name
    price = item.price
    billing_cycle = 1
    billing_cycle_unit = "Y"
  
    # What you want the button to do.
    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "a3": price,
        "p3": billing_cycle,  # duration of each unit (depends on unit)
        "t3": billing_cycle_unit,  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        'item_name': item_name,
        'custom': item.id,     # custom data, pass something meaningful here
        'currency_code': 'USD',
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment-successful')),
        "cancel_return": request.build_absolute_uri(reverse('payment-canceled')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request, 'store/cart.html', {'item':item, 'today':today, 'form':form})

def checkout(request):
    item = get_object_or_404(Item, id=request.session['item-id'])
    return render(request, 'store/checkout.html')

@csrf_exempt
def payment_successful(request):
    return render(request, 'payment/payment-successful.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/payment-canceled.html')