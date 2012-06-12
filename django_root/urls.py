from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^manage$', 'qs_counters.views.manage')
)
