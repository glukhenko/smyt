from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()



urlpatterns = patterns('',
    
    url(r'^$', 'genModels.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^dajaxice/', include('dajaxice.urls')),
    
)
