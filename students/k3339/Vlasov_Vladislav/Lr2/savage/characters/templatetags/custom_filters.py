from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    return value.startswith(arg)

@register.filter
def getSkillAndAttributesName(value):
    return value.split("_")[-1]

@register.filter
def getSkillByAttribute(value, attribute):
    print(attribute)
    return value[attribute]

@register.filter
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()