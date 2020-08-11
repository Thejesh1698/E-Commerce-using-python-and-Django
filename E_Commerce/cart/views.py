from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, reverse, redirect
from home_page.views import Product, ProductType, ProductBrand
from .models import Cart, Order
from django.contrib import messages


def cart_page(request):
    if request.user.is_authenticated:

        product_types = ProductType.objects.all()
        product_brands = ProductBrand.objects.all()

        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)

        if carts.exists():
            if orders.exists():
                prices_after_discount = []
                total_actual_cart_cost = 0.00
                total_discounted_cart_cost = 0.00
                for p in carts:
                    if p.product.product_discount != 0:
                        price = p.get_total() - p.get_total() * p.product.product_discount * 0.01
                    else:
                        price = p.get_total()
                    prices_after_discount.append(price)
                    total_actual_cart_cost += p.get_total()
                    total_discounted_cart_cost += price
                context = zip(carts, prices_after_discount)

                discounted = True
                if total_actual_cart_cost == total_discounted_cart_cost:
                    discounted = False



                return render(request, "cart_page.html", {'context': context, 'orders': orders,
                                                          'cart_size': carts.count(),
                                                          'total_actual_cart_cost': total_actual_cart_cost,
                                                          'total_discounted_cart_cost': total_discounted_cart_cost,
                                                          'discounted': discounted,
                                                          'empty': False,
                                                          'product_types': product_types,
                                                          'product_brands': product_brands, })
            else:
                return render(request, "cart_page.html", {'empty': True,
                                                          'product_types': product_types,
                                                          'product_brands': product_brands, })
        else:
            return render(request, "cart_page.html", {'empty': True,
                                                      'product_types': product_types,
                                                      'product_brands': product_brands, })
    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect("login_and_register:loginPage")


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_item, created = Cart.objects.get_or_create(
            product=product,
            user=request.user,
            purchased=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.orderitems.filter(product__slug=product.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.success(request, f"{product.product_name} quantity is updated.")
                return redirect("cart:cart_page")
            else:
                order.orderitems.add(order_item)
                messages.success(request, f"{product.product_name} is added to your cart.")
                return redirect("cart:cart_page")
        else:
            order = Order.objects.create(
                user=request.user)
            order.orderitems.add(order_item)
            messages.success(request, f"{product.product_name} is added to your cart.")
            return redirect("cart:cart_page")

    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect("login_and_register:loginPage")


def decrease_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.orderitems.filter(product__slug=product.slug).exists():
                order_item = Cart.objects.filter(product=product, user=request.user)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.error(request, f"{product.product_name} quantity is updated.")
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.error(request, f"{product.product_name} is deleted from your cart.")

            all_cart_items = Cart.objects.filter(user=request.user, purchased=False)
            if all_cart_items.count() == 0:
                order_qs.delete()

            return redirect("cart:cart_page")
        else:
            messages.error(request, f"{product.product_name} is not present in your cart.")
            return redirect("cart:cart_page")

    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect("login_and_register:loginPage")


def remove_cart(request, slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, slug=slug)
        all_cart_items = Cart.objects.filter(user=request.user, purchased=False)

        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(product__slug=product.slug).exists():
                order_item = Cart.objects.filter(product=product, user=request.user)[0]
                order.orderitems.remove(order_item) # this will take care of deletion of item in cart table in db too
                order_item.delete()
                messages.error(request, f"{product.product_name} is removed from your cart.")
            else:
                messages.error(request, f"{product.product_name} is not present in your cart.")

            if all_cart_items.count() == 0:
                order_qs.delete()

        else:
            messages.error(request, f"{product.product_name} is not present in your cart.")

        return redirect("cart:cart_page")
    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect("cart:cart_page")


def my_orders(request):
    if request.user.is_authenticated:
        product_types = ProductType.objects.all()
        product_brands = ProductBrand.objects.all()

        order_qs = Order.objects.filter(user=request.user, ordered=True).order_by('-id')
        isempty = True
        if order_qs.count() != 0:
            messages.info(request, "We are working hard to deliver your orders soon :)")
            isempty = False
        return render(request, "my_orders.html", {'orders': order_qs, 'isempty': isempty,
                                                  'product_types': product_types,
                                                  'product_brands': product_brands,})
    else:
        messages.error(request, "Opps! Seems like you are logged out. Please login first!!")
        return redirect('login_and_register:loginPage')