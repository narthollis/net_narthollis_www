from django.conf.urls import patterns, include, url

from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'net_narthollis_www.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='blog', permanent=True)),
    
    url(r'^blog/', include('zinnia.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^pygments/style.css', 'zinnia_theme_netnarthollis.views.get_pygments_css', name="pygments_css"),

    #url(r'^xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc'),

    url(r'^admin/', include(admin.site.urls)),
)
