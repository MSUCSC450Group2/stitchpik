from django.conf.urls import patterns, include, url
from django.contrib import admin
from login.views import *
from image_manipulation.views import *
from django.contrib.auth.views import login, password_reset, password_reset_confirm, password_reset_done, password_reset_complete
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'login.views.index', name='index'),
     
    # Examples:
    # url(r'^$', 'stitchpick.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^login/$', loginTry, name='login'),
    url(r'^accounts/login/$', loginTry),
    url(r'^admin/$', include(admin.site.urls)), 
    url(r'^logout/$', logoutPage),
    url(r'^registration/$', registration, name ='signup'),
    url(r'^registration/success/$', registrationSuccess),
    url(r'^application/$', fetchApplication, name='application'),
    
    # Change Password URLs:
    url(r'^accounts/password_change/$', 
        'django.contrib.auth.views.password_change', 
        {'post_change_redirect' : '/accounts/password_change/done/'}, ), 
    url(r'^accounts/password_change/done/$', 
        'django.contrib.auth.views.password_change_done'),
    # Password Reset URLs:
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'accounts/forgot_password.html',\
                               'post_reset_redirect' : '/user/password/reset/done/'}, name="reset_password"),
    url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),   
    url(r'^user/password/reset/confirm/$', 
             'django.contrib.auth.views.password_reset_confirm'),
    url(r'^user/password/reset/complete/$', 
             'django.contrib.auth.views.password_reset_complete'),
    #
    
    )
  