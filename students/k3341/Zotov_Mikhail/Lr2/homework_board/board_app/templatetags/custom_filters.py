from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    try:
        return value - arg
    except (TypeError, ValueError):
        return 0


@register.filter
def get_item(dictionary, key):
    """Возвращает элемент из словаря по ключу."""
    return dictionary.get(key)
