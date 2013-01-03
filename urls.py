from django.conf.urls.defaults import url, patterns
from eulfedora.views import raw_datastream, raw_audit_trail


urlpatterns = patterns(
    'repo.views',
    url('^upload/$', 'upload', name='upload'),
    url(r'^objects/(?P<pid>[^/]+)/$', 'display', name='display'),
    url(r'^(?P<pid>[^/]+)/DC/edit/$', 'edit', name='edit'),
)
urlpatterns += patterns(
    '',
    url(r'^(?P<pid>[^/]+)/(?P<dsid>(MODS|RELS-EXT|DC))/$', raw_datastream),
    url(r'^(?P<pid>[^/]+)/AUDIT/$', raw_audit_trail),
)
