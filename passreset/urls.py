from django.conf.urls.defaults import patterns,  url
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

urlpatterns = patterns('django.contrib.auth.views', 
    url(r'^$', 'password_reset', name='password-reset'), 
    url(r'^done/$', 'password_reset_done', name='password-reset-done'), 
    url(r'^confirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'password_reset_confirm', name='password-reset-confirm'), 
    url(r'^complete/$', 'password_reset_complete',
            {'extra_context':{'login_url':lazy(reverse, unicode)('admin:index')}},
            name='password-reset-complete')
)
