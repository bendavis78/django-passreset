from __future__ import unicode_literals

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import loader, RequestContext
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetForm(auth_forms.PasswordResetForm):
    """
    Kludge to get around the fact that the password email context does not
    include current_app. This is necessary when using namespaced urls.

    Copied from: `contrib.auth.forms.PasswordResetForm.save()` @django-1.7b4
    """
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                'current_app': self.current_app
            }
            context_instance = RequestContext(request)
            subject = loader.render_to_string(
                subject_template_name, c, context_instance)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(
                email_template_name, c, context_instance)

            if html_email_template_name:
                html_email = loader.render_to_string(
                    html_email_template_name, c, context_instance)
            else:
                html_email = None
            send_mail(subject, email, from_email, [user.email],
                      html_message=html_email)


def passreset_form(current_app):
    """
    Form factory which adds current_app to the PasswordResetForm. This is a
    shortcut which keeps us from having to override the view from contrib.auth.
    """
    return type(b'PasswordResetForm', (PasswordResetForm,), {
        b'current_app': current_app,
        b'__module__': __name__
    })
