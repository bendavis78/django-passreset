from django.core.urlresolvers import reverse
from django.conf import settings
from django.conf.urls.defaults import patterns,  url
from django.utils.functional import lazy
from django.contrib import admin
from passreset.forms import passreset_form

# override default admin login template
admin.site.login_template = 'passreset/admin/login.html'

def urls_ns(namespace=None, login_url=None):
    """
    Creates namespaced urlpatterns with the given namespace
    """
    if login_url is None:
        login_url = settings.LOGIN_URL
    post_reset_redirect_done = lazy(reverse, unicode)('passreset:password-reset-done')
    post_reset_redirect_complete = lazy(reverse, unicode)('passreset:password-reset-complete')
    password_reset_form = passreset_form(namespace) 
    return (patterns(
        'django.contrib.auth.views', 
        url(r'^$', 'password_reset', 
                name='password-reset',
                kwargs={'post_reset_redirect': post_reset_redirect_done,
                        'password_reset_form': password_reset_form,
                        'current_app': namespace}), 
        url(r'^done/$', 'password_reset_done', 
                name='password-reset-done', 
                kwargs={'current_app': namespace}),
        url(r'^confirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'password_reset_confirm',
                name='password-reset-confirm',
                kwargs={'post_reset_redirect': post_reset_redirect_complete,
                        'current_app': namespace}),
        url(r'^complete/$', 'password_reset_complete',
                name='password-reset-complete',
                kwargs={'extra_context':{'login_url':login_url},
                        'current_app': namespace}),
    ), 'passreset', namespace)

urls = urls_ns()
admin_urls = urls_ns('admin-passreset', 'admin:login')
