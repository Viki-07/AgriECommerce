from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by arg"""
    try:
        return round(float(value) * float(arg), 2)
    except (ValueError, TypeError):
        return ''
