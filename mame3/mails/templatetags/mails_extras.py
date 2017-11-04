from django import template
from babel.dates import format_date

register = template.Library()

@register.filter
def preaddr(value, arg):
    addr = ''
    if value:
        addr = '%s%s' % (arg, value)
    return addr

@register.filter
def thaidate(value):
    dm = format_date(value, 'd MMM', locale='th_TH')
    y = value.year + 543
    return '%s %s' % (dm, y)
