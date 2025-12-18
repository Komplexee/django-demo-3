from django import template

register = template.Library()

@register.filter
def discounted_price(price, discount):
    if discount > 0:
        return price - (price * discount / 100)
    return price

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def div(value, arg):
    return value / arg
