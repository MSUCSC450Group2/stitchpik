from django.conf.urls import patterns, include, url
from django.contrib import admin
from login.views import *
from image_manipulation.views import *
admin.autodiscover()
#    ^ this might be need to be changed to point correctly

urlpatterns = patterns('',
    url(r'^$', 'login.views.index', name='index'),	       
    # Examples:
    # url(r'^$', 'stitchpick.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', 'django.contrib.auth.views.login'),
	#          \/ will be changed to main index view
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
        'django.contrib.auth.views.password_change_done',{'template_name': 'done.html'}),
    
)
