from django import template

register = template.Library()

@register.filter
def pairs(value):
    values = value.split('|')
    return zip(values[::3], values[1::3], values[2::3])
