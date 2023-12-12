from django import template

register = template.Library()

@register.filter
def censor(value):
    '*'
    return censored_value