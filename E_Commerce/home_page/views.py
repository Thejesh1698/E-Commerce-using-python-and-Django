from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .models import Product, ProductType, ProductBrand, UserProfile
from django.contrib import messages


def home(request):

    product_types = ProductType.objects.all()
    product_brands = ProductBrand.objects.all()

    products = Product.objects.all()
    prices = []

    for p in products:
        if p.product_discount != 0:
            price = p.product_price-p.product_price*p.product_discount*0.01
        else:
            price = p.product_price
        prices.append(price)

    context = zip(products, prices)

    return render(request, "home.html", {'context': context,
                                         'product_types': product_types,
                                         'product_brands': product_brands, })


def base(request):
    product_types = ProductType.objects.all()
    product_brands = ProductBrand.objects.all()

    return render(request, "base.html", {'product_types': product_types,
                                         'product_brands': product_brands, })


def my_profile(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)

        product_types = ProductType.objects.all()
        product_brands = ProductBrand.objects.all()

        male = False
        female = False
        prefer_not_to_say = False
        gender = user_profile.gender

        if gender == "male":
            male = True
        elif gender == "female":
            female = True
        elif gender == "Prefer not to say":
            prefer_not_to_say = True

        dob = user_profile.date_of_birth

        return render(request, 'profile.html', {'email': request.user.email,
                                                'amount': user_profile.user_wallet,
                                                'username': request.user.username,
                                                'phonenumber': user_profile.phone_number,
                                                'male': male, 'female': female,
                                                'prefer_not_to_say': prefer_not_to_say, 'dob': dob,
                                                'product_types': product_types,
                                                'product_brands': product_brands,
                                                'billing_addresses': user_profile.billing_addresses.all, })

    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect("login_and_register:loginPage")


def change_profile(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)

        button_name = request.POST['save']

        if button_name == "username":
            request.user.username = request.POST['username']
        elif button_name == "phonenumber":
            phone_number = request.POST['phonenumber']
            if len(str(phone_number)) < 10 or len(str(phone_number)) > 19 or int(phone_number) >= 9223372036854775807:
                messages.error(request, "Please give a valid phone number!!")
                return redirect("home_page:my_profile")

            user_profile.phone_number = request.POST['phonenumber']
        elif button_name == "gender":
            user_profile.gender = request.POST['gender']
        else:
            user_profile.date_of_birth = request.POST['dob']

        user_profile.save()
        request.user.save()
        messages.success(request, "Hurray!! your profile has been updated")
        return redirect("home_page:my_profile")
    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect("login_and_register:loginPage")
