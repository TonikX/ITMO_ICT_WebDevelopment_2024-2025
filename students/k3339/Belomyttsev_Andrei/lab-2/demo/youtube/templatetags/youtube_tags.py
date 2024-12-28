from django import template

register = template.Library()

@register.filter()
def intformat(n):
  return ((f'{str(n)[:-9]}.{str(n)[-9]}B' if n >= 1000000000 else f'{str(n)[:-6]}.{str(n)[-6]}M') if n >= 1000000 else f'{str(n)[:-3]}.{str(n)[-3]}K') if n >= 1000 else n