import random

from django import template

register = template.Library()


@register.filter
def times(number):
    return range(number)


@register.filter
def random_user_id(value):
    number = random.randint(100000, 999999)
    return number
