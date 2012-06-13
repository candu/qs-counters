from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'qs_counters.views.home'),
    url(r'^add$', 'qs_counters.views.add'),
    url(r'^delete$', 'qs_counters.views.delete'),
    url(r'^update$', 'qs_counters.views.update'),
    url(r'^stats$', 'qs_counters.views.stats')
)
