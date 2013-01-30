from django.conf.urls import patterns, include, url
from django_vingd.urls import VingdUrls

urlpatterns = patterns('',
    url(r'^$', 'base.views.home', name='home'),
    url(r'^popup/$', 'base.views.popup', name='popup'),
    (r'^vgd/', include(VingdUrls())),
)
