from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserDetails,address,Payment
from product.models import  Bill

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)


@receiver(post_save, sender=Bill)
def create_bill(sender,instance, created, **kwargs):
    if created:
        address.objects.create(bill = instance)
        Payment.objects.create(bill = instance)
