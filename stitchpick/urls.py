from django.conf.urls import patterns, include, url
from django.contrib import admin
from .login.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stitchpick.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^$', loginTry),
    url(r'^accounts/login/$', loginTry),
    url(r'^admin/$', include(admin.site.urls)), 
    url(r'^logout/$', logoutPage),
    url(r'^registration/$', registration),
    url(r'^registration/success/$', registrationSuccess),
    url(r'^home/$', home),
)
