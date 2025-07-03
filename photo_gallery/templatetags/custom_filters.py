from django import template

register = template.Library()

@register.filter(name='capitalize_words')
def capitalize_words(value):
    """Capitalizes every word in a string."""
    return ' '.join(word.capitalize() for word in value.split())

@register.filter(name='split_tags')
def split_tags(value):
    """Splits a comma-separated string of tags into a list."""
    if isinstance(value, str):
        return [tag.strip() for tag in value.split(',')]
    return []
@register.filter(name='trim')
def trim(value):
    """Trims whitespace from a string."""
    return value.strip()
