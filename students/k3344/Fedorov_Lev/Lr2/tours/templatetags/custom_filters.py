from django import template

register = template.Library()

@register.filter
def has_travelagency(user):
    return hasattr(user, 'travelagency')