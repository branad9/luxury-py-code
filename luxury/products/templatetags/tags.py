from django import template

register = template.Library()

@register.filter
def unslug(name):
    if name is not None:
        return name.replace("-", " ")
    else:
        return ''
    