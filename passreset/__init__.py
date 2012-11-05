from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.conf.urls.defaults import patterns,  url
from django.contrib import admin
from passreset.forms import passreset_form

# override default admin login template
admin.site.login_template = 'passreset/admin/login.html'

def urls_ns(namespace, login_url=None, tpl_path=None):
    """
    Creates namespaced urlpatterns with the given namespace
    """
    if login_url is None:
        login_url = settings.LOGIN_URL
    post_reset_redirect_done = reverse_lazy('passreset:password-reset-done', current_app=namespace)
    post_reset_redirect_complete = reverse_lazy('passreset:password-reset-complete', current_app=namespace)
    password_reset_form = passreset_form(namespace) 
    if tpl_path is None:
        tpl_path = namespace is not None and namespace.replace('-', '_') or 'passreset'
    tpl = lambda name: [
        '{}/{}'.format(tpl_path, name),
        'passreset/{}'.format(name)
    ]
    return (patterns(
        'django.contrib.auth.views', 
        url(r'^$', 'password_reset', 
                name='password-reset',
                kwargs={'post_reset_redirect': post_reset_redirect_done,
                        'password_reset_form': password_reset_form,
                        'template_name': tpl('password_reset_form.html'),
                        'email_template_name': tpl('password_reset_email.html'),
                        'subject_template_name': tpl('password_reset_subject.txt'),
                        'current_app': namespace}), 
        url(r'^done/$', 'password_reset_done', 
                name='password-reset-done', 
                kwargs={'template_name': tpl('password_reset_done.html'),
                        'current_app': namespace}),
        url(r'^confirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'password_reset_confirm',
                name='password-reset-confirm',
                kwargs={'post_reset_redirect': post_reset_redirect_complete,
                        'template_name': tpl('password_reset_confirm.html'),
                        'current_app': namespace}),
        url(r'^complete/$', 'password_reset_complete',
                name='password-reset-complete',
                kwargs={'extra_context':{'login_url':login_url},
                        'template_name': tpl('password_reset_complete.html'),
                        'current_app': namespace}),
    ), 'passreset', namespace)

urls = urls_ns(None)
admin_urls = urls_ns('admin-passreset', reverse_lazy('admin:index'), tpl_path='registration')
