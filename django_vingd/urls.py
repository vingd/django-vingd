from django.conf import settings
from django.conf.urls.defaults import patterns, url

from .views import OrderView, VerifyView
from .util import initialize_all_django_models

class VingdUrls():
    urlpatterns = None
    
    def __init__(self, order_view=None, verify_view=None):
        initialize_all_django_models()
        order_view = order_view or OrderView
        verify_view = verify_view or VerifyView
        self.urlpatterns = patterns('',
            url(r'^order/(?P<nametag>\w+)/$', order_view.as_view(), name='vingd_order'),
            url(r'^verify/$', verify_view.as_view(), name='vingd_verify'),
        )
