from django import template

register = template.Library()

@register.filter(name='split_tags')
def split_tags(value):
    return value.split(',')

@register.filter(name='trim')
def trim(value):
    return value.strip()
