from __future__ import unicode_literals

from django import VERSION as django_version
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.template.loader import select_template
from passreset.forms import passreset_form

default_app_config = 'passreset.apps.AppConfig'
app_label = __name__.split('.')[-1]

# override default admin login template
admin.site.login_template = 'passreset/admin/login.html'


def urls_ns(namespace=app_label, login_url=None, tpl_path=None):
    """
    Creates namespaced urlpatterns with the given namespace, and returns a
    3-tuple for use with `include()`
    """
    if login_url is None:
        login_url = settings.LOGIN_URL

    post_reset_redirect_done = reverse_lazy('passreset:done',
                                            current_app=namespace)
    post_reset_redirect_complete = reverse_lazy('passreset:complete',
                                                current_app=namespace)
    password_reset_form = passreset_form(namespace)

    if tpl_path is None and namespace is not None:
        tpl_path = namespace.replace('-', '_') or 'passreset'

    tpl = lambda name: [
        '{}/{}'.format(tpl_path, name),
        'passreset/{}'.format(name)
    ]

    # django 1.6 changed the uidb32 arg to uidb64
    if django_version[1] < 6:
        uid_arg = 'uidb32'
    else:
        uid_arg = 'uidb64'

    extra_context = {
        'login_url': login_url,
        'base_tpl': lambda: select_template(tpl('base.html')),
        'uid_arg': uid_arg
    }

    def password_reset_confirm(*args, **kwargs):
        # hack to make backward compatible uidb32/uidb64 arg
        if 'uid' in kwargs:
            kwargs[uid_arg] = kwargs.pop('uid')
        return views.password_reset_confirm(*args, **kwargs)

    from django.contrib.auth import views
    return ([
        url(r'^$', views.password_reset, name='reset-password',
            kwargs={
                'post_reset_redirect': post_reset_redirect_done,
                'password_reset_form': password_reset_form,
                'template_name': tpl('reset_password.html'),
                'email_template_name': tpl('email.html'),
                'subject_template_name': tpl('subject.txt'),
                'current_app': namespace,
                'extra_context': extra_context
            }),
        url(r'^done/$', views.password_reset_done, name='done',
            kwargs={
                'template_name': tpl('done.html'),
                'current_app': namespace,
                'extra_context': extra_context
            }),
        url(r'^confirm/(?P<uid>[-\w]+)/(?P<token>[-\w]+)/$',
            password_reset_confirm, name='confirm',
            kwargs={
                'post_reset_redirect': post_reset_redirect_complete,
                'template_name': tpl('confirm.html'),
                'current_app': namespace,
                'extra_context': extra_context
            }),
        url(r'^complete/$', views.password_reset_complete, name='complete',
            kwargs={
                'template_name': tpl('complete.html'),
                'current_app': namespace,
                'extra_context': extra_context
            }),
    ], 'passreset', namespace)

urls = urls_ns()
admin_urls = urls_ns(
    'admin-passreset', reverse_lazy('admin:index'), tpl_path='registration')
