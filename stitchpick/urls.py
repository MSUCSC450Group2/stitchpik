from django.conf.urls import patterns, include, url
from django.contrib import admin
from login.views import *
#    ^ this might be need to be changed to point correctly
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'WebPages.views.home', name='home'),		
    # Examples:
    # url(r'^$', 'stitchpick.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', 'django.contrib.auth.views.login'),
	#          \/ will be changed to main index view
    url(r'^$', loginTry),
    url(r'^accounts/login/$', loginTry),
    url(r'^admin/$', include(admin.site.urls)), 
    url(r'^logout/$', logoutPage),
    url(r'^registration/$', registration, name ='signup'),
    url(r'^registration/success/$', registrationSuccess),
    url(r'^home/$', home),
)

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL,
			document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL,
			document_root=settings.MEDIA_ROOT)
  