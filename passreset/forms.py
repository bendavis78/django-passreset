from django.contrib.auth import forms as auth_forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import loader, Context
from django.utils.http import int_to_base36


class PasswordResetForm(auth_forms.PasswordResetForm):
    """
    Kludge to get around the fact that the password email context does not
    include current_app. This is necessary when using namespaced urls.
    """
    current_app = None

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        from django.core.mail import send_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            context_instance = Context(current_app=self.current_app)
            subject = loader.render_to_string(
                subject_template_name, c, context_instance)

            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(
                email_template_name, c, context_instance)
            send_mail(subject, email, from_email, [user.email])


def passreset_form(current_app):
    """
    Form factory which adds current_app to the PasswordResetForm. This is a
    shortcut which keeps us from having to override the view from contrib.auth.
    """
    return type('PasswordResetForm', (PasswordResetForm,), {
        'current_app': current_app
    })
