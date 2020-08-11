from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from billing.models import BillingAddress
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class ProductType(models.Model):
    type = models.CharField(max_length=300)
    slug = models.SlugField(default="default_Type_slug_name")

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("product_detail:DisplayTypeProducts", kwargs={
            'slug': self.slug, 'value': "low",
        })


class ProductBrand(models.Model):
    brand = models.CharField(max_length=300)
    slug = models.SlugField(default="default_Brand_slug_name")

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse("product_detail:DisplayBrandProducts", kwargs={
            'slug': self.slug, 'value': "low",
        })


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='web_templates/static/Images')
    product_price = models.IntegerField()
    product_discount = models.IntegerField()
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product_brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    product_stock = models.IntegerField(default=1)
    product_rating = models.IntegerField(default=1)
    product_description = models.TextField(default="It's a good product to buy :)")
    slug = models.SlugField(default="default_slug_name")

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("product_detail:DescribeProduct", kwargs={
            'slug': self.slug
        })

    def get_cart_url(self):
        return reverse('cart:add_to_cart', kwargs={'slug': self.slug})

    def get_decrease_cart_url(self):
        return reverse('cart:decrease_cart', kwargs={'slug': self.slug})

    def get_remove_cart_url(self):
        return reverse('cart:remove_cart', kwargs={'slug': self.slug})


User = get_user_model()


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_wallet = models.IntegerField(default=5000)
    billing_addresses = models.ManyToManyField(BillingAddress)
    phone_number = models.BigIntegerField()
    gender = models.CharField(max_length=100, default="Prefer not to say")
    date_of_birth = models.DateField(default=datetime.date.today)

    @classmethod
    def create(cls, user, user_wallet):
        user_profile = cls(user=user, user_wallet=user_wallet)
        return user_profile


class UsernameOrEmailBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs['username']
        password = kwargs['password']
        try:
            customers = User.objects.filter(email=email)
            if customers.count() !=0:
                customer = customers[0]
                if customer is not None:
                    if customer.check_password(password) is True:
                        return customer
                    else:
                        return None
                else:
                    return None
            else:
                return None
        except User.DoesNotExist:
            return None
