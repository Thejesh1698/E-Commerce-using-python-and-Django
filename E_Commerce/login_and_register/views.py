from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from home_page.models import UserProfile, ProductType, ProductBrand


def login_page(request):
    product_types = ProductType.objects.all()
    product_brands = ProductBrand.objects.all()

    return render(request, "login.html", {'product_types': product_types,
                                          'product_brands': product_brands, })


def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out!")
    return redirect('/')


def login_or_register(request):

    button_name = request.POST['login_or_register_button']

    if button_name == "Login":
        user = authenticate(username=request.POST['username1'], password=request.POST['password1'])

        if user is not None:
            login(request, user)
            messages.success(request, "Dear "+request.POST['username1']+", You are securely logged in!")
            return redirect('/')
        else:
            messages.error(request, "Sorry Human. Invalid credentials!")
            return redirect('/loginPage/')
    elif button_name == "Register":

        # need to also check if the username/password fields are empty in the form
        if User.objects.filter(username=request.POST['username2']).exists():
            messages.error(request, "Unlucky. Username is already taken by someone. Try another!")
            return redirect('/loginPage/')
        elif User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, "Strangely, this email already exists."
                                    " Use it to login or use different email to create account!")
            return redirect('/loginPage/')
        else:
            user = User.objects.create_user(username=request.POST['username2'], password=request.POST['password2'],
                                            email=request.POST['email'])
            user.save()
            user_profile = UserProfile.create(user, 5000)
            user_profile.save()
            messages.success(request, "Congratulations. You are now part of E_Commerce. "
                                      "Please log in to use our services!")
            return redirect('/loginPage/')
