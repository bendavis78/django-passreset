=====================
Django Password Reset
=====================
I couldn't find a simple way to add password reset functionality to the vanilla Django admin site, hence this tiny little app.

Just add "passreset" to ``INSTALLED_APPS``, and the add this line to your urls.py, right above your admin url::

    ...
    url(r'^admin/passreset/', include('passreset.urls')),
    url(r'^admin/', include(admin.site.urls)),
    ...

The app takes care of the rest, with the help of django's built-in password reset workflow.
