from django import template

register = template.Library()


@register.filter(name='range_filter')
def range_filter(value):
    if len(value) <= 500:
        return value
    return value[0:500] + "..."
