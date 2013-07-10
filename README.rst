=====================
Django Password Reset
=====================
This app simplifies the process for adding password reset functionality to your
site. It takes advantage of django's exising password reset workflow, but
simplifies the process of adding urls to your site. This also allows you to
create multiple password reset workflows for one site using namespacing.

Just add "passreset" to ``INSTALLED_APPS``, and the add this line to your
urlpatterns in urls.py:

.. code:: python

    url(r'^profile/passreset/', include('passreset.urls')),

The app takes care of the rest, with the help of django's built-in password
reset workflow.

To quickly add password reset functionality to your existing admin, just change
the above line to the following:

.. code:: python
    
    from django.conf.urls.defaults import patterns, url, include
    import passreset

    urlpatterns += patterns('',
      url(r'^admin/passreset/', include(passreset.admin_urls),
      url(r'^admin/', include(admin.site.urls)),
    )

As an added convenience, the passreset app automatically overrides the default
admin site's login template to add a "forgot password?" link.

If you need multiple password-reset workflows for one site, you can use the
``urls_ns()`` function:

.. code:: python

    include(passreset.urls_ns('profile-passreset', login_url='/profile/login'))

If login_url is not supplied, settings.LOGIN_URL is used. You can also pass a 
``template_path`` argument to specify a base path for templates used in the app
instance.

The ``passreset.admin_urls`` urlconf is basically a convenience shortcut for
``passreset.urls_ns('admin-passreset', login_url='admin:login')``. As an added
conenience, the passreset app overrides the default admin login template with a
"Forgot password?" link, which basically looks like this:

.. code:: html

   <a href="{% url admin-passreset:password-reset %}">Forgot password?</a>

Putting it all together, you can use multiple password reset workflows,
including one for your admin, like so:

.. code:: python

    urlpatterns += patterns('',
      url(r'^admin/passreset/', include(passreset.admin_urls)),
      url(r'^admin/', include(admin.site.urls)),
      url(r'^profile/passreset', include(passreset.urls_ns('profile-passreset',
              login_url='/profile/login')),
    )

If we're not needing any other password reset urls, the above example can be
rewritten like so:

.. code:: python
    
    urlpatterns += patterns('',
      url(r'^admin/passreset/', include(passreset.admin_urls)),
      url(r'^admin/', include(admin.site.urls)),
      url(r'^profile/passreset', include('passreset.urls')),
    )

This essentially sets up the urls with the default namespace of "passreset". So,
to reverse the url, you'd use ``reverse("passreset:password-reset")``.
