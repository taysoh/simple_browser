from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'browser.views.home', name='home'),
    url(r'^connect_existed/', 'browser.views.connect', name='connect'),
    url(r'^go/', 'browser.views.go_to', name='chdir'),
    )

urlpatterns += staticfiles_urlpatterns()


