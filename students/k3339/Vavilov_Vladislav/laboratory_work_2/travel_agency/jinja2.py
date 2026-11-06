from django.urls import reverse
from jinja2 import Environment


def url(name, *args):
    return reverse(name, args=args)


def environment(**options):
    env = Environment(**options)
    env.globals.update(url=url)
    return env
