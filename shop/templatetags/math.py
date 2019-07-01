from django import template

register = template.Library()


@register.filter
def modulo(value, arg):
    return value % arg


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def multiply(value, arg):
    return value * arg
