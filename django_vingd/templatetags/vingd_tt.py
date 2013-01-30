from django.conf import settings
from django.template import Library

from decimal import Decimal

from .. import consts

register = Library()

@register.inclusion_tag("vingd/vingd_scripts.html")
def vingd_scripts():
    return {
        'SITE_URL': settings.SITE_URL,
        'STATIC_URL': settings.STATIC_URL,
        'VINGD_CDN': consts.VINGD_CDN,
        'VINGD_FRONTEND': consts.VINGD_FRONTEND,
    }

# Convert integer to OKA
@register.filter
def int_vingd(int_value):
    if type(int_value)!=int:
        return None
    return Decimal(int_vingd_string(int_value))

def int_vingd_string(int_value):
    if int_value<0:
        return "-" + int_vingd_string(-int_value)
    start = int_value/100
    end = int_value%100
    if (end<10):
        end = '0' + end.__str__()
    return start.__str__() + '.' + end.__str__()
