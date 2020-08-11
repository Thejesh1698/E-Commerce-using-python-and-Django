from django.db import models
from django.contrib.auth import get_user_model
from home_page.models import Product
from billing.models import BillingAddress
import datetime


User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.product.product_name}'

    def get_total(self):
        total = self.product.product_price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal


class Order(models.Model):
    orderitems  = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=200, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, default=0)
    delivered = models.BooleanField(default=False)
    ordered_date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    def get_totals(self):
        total = 0
        for order_product in self.orderitems.all():
            total += order_product.get_total()

        return total
