from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'qs_counters.views.home'),
    url(r'^add$', 'qs_counters.views.add'),
    url(r'^view/(?P<id>\d+)$', 'qs_counters.views.view'),
    url(r'^update/(?P<id>\d+)$', 'qs_counters.views.update'),
    url(r'^delete/(?P<id>\d+)$', 'qs_counters.views.delete'),
    url(r'^stats_all$', 'qs_counters.views.stats_all'),
    url(r'^stats/(?P<id>\d+)$', 'qs_counters.views.stats'),
)
