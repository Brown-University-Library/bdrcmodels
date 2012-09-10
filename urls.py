from django.conf.urls.defaults import *

urlpatterns = patterns('repo.views',
        url('^upload/$', 'upload', name = 'upload'),
        url(r'^objects/(?P<pid>[^/]+)/$', 'display', name='display'),
        )
