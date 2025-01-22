# tours/templatetags/custom_tags.py

from django import template
import hashlib

register = template.Library()

@register.filter
def gravatar(email, size=50):
    """
    Возвращает URL Gravatar для данного email.
    """
    email = email.lower().strip()
    hash_email = hashlib.md5(email.encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_email}?s={size}&d=identicon"