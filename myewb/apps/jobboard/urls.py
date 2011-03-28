from django.conf.urls.defaults import *

urlpatterns = patterns('jobboard.views',
    url(r'^$', view='list', name="jobboard_list"),
    url(r'^(?P<id>\d+)/$', view='detail', name="jobboard_detail"),

    url(r'^new/$', view='edit', name="jobboard_new"),
    url(r'^(?P<id>\d+)/edit/$', view='edit', name="jobboard_edit"),
    
    url(r'^(?P<id>\d+)/bid/$', view='bid', name="jobboard_bid"),
    url(r'^(?P<id>\d+)/bid/cancel/$', view='bid_cancel', name="jobboard_bid_cancel"),
    url(r'^(?P<id>\d+)/watch/$', view='watch', name="jobboard_watch"),
    url(r'^(?P<id>\d+)/watch/cancel/$', view='watch_cancel', name="jobboard_watch_cancel"),

    url(r'^(?P<id>\d+)/close/$', view='close', name="jobboard_close"),
    url(r'^(?P<id>\d+)/open/$', view='open', name="jobboard_open"),

    url(r'^(?P<id>\d+)/accept/(?P<username>[\w\._-]+)/$', view='accept', name="jobboard_accept"),
    url(r'^(?P<id>\d+)/accept/(?P<username>[\w\._-]+)/cancel/$', view='accept_cancel', name="jobboard_accept_cancel"),
)