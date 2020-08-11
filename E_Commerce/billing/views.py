from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils.crypto import get_random_string
import datetime
from .models import BillingAddress
from home_page.models import UserProfile, ProductType, ProductBrand
from cart.models import Order, Cart
from django.contrib import messages


def address_page(request):
    if request.user.is_authenticated:
        product_types = ProductType.objects.all()
        product_brands = ProductBrand.objects.all()

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            storage = get_messages(request)

            if len(storage) == 0:
                messages.info(request, "You are just two steps away from placing your order")

            return render(request, "billing_address.html", {'order': order,
                                                            'product_types': product_types,
                                                            'product_brands': product_brands, })
        else:
            messages.error(request, "Unfortunately, your cart is empty. Please fill your cart!!")
            return redirect("cart:cart_page")
    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect("login_and_register:loginPage")


def proceed_to_payment(request):
    if request.user.is_authenticated:
        product_types = ProductType.objects.all()
        product_brands = ProductBrand.objects.all()

        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        phone_number = request.POST['phone_number']

        if len(str(phone_number)) < 10 or len(str(phone_number)) > 19 or int(phone_number) >= 9223372036854775807:
            messages.error(request, "Please give a valid phone number!!")
            return redirect("billing:address_page")

        billing_address = BillingAddress.create(request.user, address, zip_code, city, state, country, phone_number)
        billing_address.save()

        user_profiles = UserProfile.objects.filter(user=request.user)
        user_profile = user_profiles[0]
        user_profile.billing_addresses.add(billing_address)
        user_profile.save()

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order = order_qs[0]
        order.billing_address = billing_address
        order.save()

        cartitems = Cart.objects.filter(user=request.user, purchased=False)
        order_cost = 0.00
        for item in cartitems:
            if item.product.product_discount != 0:
                order_cost += item.get_total() - item.get_total() * item.product.product_discount * 0.01
            else:
                order_cost += item.get_total()

        if order_cost < 500:
            order_cost += 100

        user_profiles = UserProfile.objects.filter(user=request.user)
        user_profile = user_profiles[0]

        resultant_wallet_amount = user_profile.user_wallet - order_cost

        messages.info(request, "You are just a step away from placing your order")
        return render(request, "payment.html", {'order_cost': order_cost,
                                                'wallet_amount': user_profile.user_wallet,
                                                'resultant_amount': resultant_wallet_amount,
                                                'product_types': product_types,
                                                'product_brands': product_brands, })
    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect("login_and_register:loginPage")


def pay(request):
    if request.user.is_authenticated:
        status = False
        product_types = ProductType.objects.all()
        product_brands = ProductBrand.objects.all()

        order = Order.objects.get(user=request.user, ordered=False)
        orderid = get_random_string(length=8, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        order.orderId = f'#{request.user}{orderid}'

        paymentid = get_random_string(length=8, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        order.paymentId = f'#{paymentid}{request.user}'
        order.ordered = True
        order.ordered_date = datetime.date.today()
        order.save()
        cartitems = Cart.objects.filter(user=request.user, purchased=False)
        order_cost = 0.00
        for item in cartitems:
            if item.product.product_discount != 0:
                order_cost = item.get_total() - item.get_total() * item.product.product_discount * 0.01
            else:
                order_cost = item.get_total()
            item.purchased = True
            item.save()
        user_profiles = UserProfile.objects.filter(user=request.user)
        user_profile = user_profiles[0]
        user_profile.user_wallet -= int(order_cost)
        user_profile.save()
        status = True

        messages.success(request, "Payment Successful")
        return render(request, "payment_done.html", {'status': status,
                                                     'product_types': product_types,
                                                     'product_brands': product_brands,})
    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect('login_and_register:loginPage')
