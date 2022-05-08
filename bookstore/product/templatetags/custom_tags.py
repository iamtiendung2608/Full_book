from distutils.command.register import register
from django import template
from django.contrib.auth.models import Group
from account.models import address, Payment


register = template.Library()
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name= group_name)
    return True if group in user.groups.all() else False

@register.filter(name='get_address')
def get_address(bill):
    ele = address.objects.get(bill = bill)
    return ele

@register.filter(name='get_payment')
def get_payment(bill):
    payment = Payment.objects.get(bill = bill)
    return payment
