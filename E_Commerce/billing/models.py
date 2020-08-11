from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    phone_number = models.BigIntegerField()

    @classmethod
    def create(cls, user, address, zipcode, city, state, country, phone_number):
        billing_address = cls(user=user, address=address, zipcode=zipcode, city=city, state=state, country=country, phone_number=phone_number)
        return billing_address


