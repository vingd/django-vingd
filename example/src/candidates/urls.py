from django.conf.urls import patterns, include, url

from django_vingd.models import VingdMeta
from base.models import VoteOrder

VingdMeta.register([VoteOrder, ])

urlpatterns = patterns('',
    url(r'^$', 'base.views.home', name='home'),
    url(r'^popup/$', 'base.views.popup', name='popup'),
    (r'^vgd/', include('django_vingd.urls')),
)
