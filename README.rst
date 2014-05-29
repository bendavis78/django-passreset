=====================
Django Password Reset
=====================
This app simplifies the process for adding password reset functionality to your
site. It takes advantage of django's exising password reset workflow, but
simplifies the process of adding urls to your site. This also allows you to
create multiple password reset workflows for one site using namespacing.


Installation
------------

Just add `"passreset"` to `INSTALLED_APPS`, and include `passreset.urls`
in your urlconf module:

.. code:: python

    from django.conf.urls import url, include
    import passreset
    urlpatterns = [
        #...
        url(r'^profile/passreset/', include(passreset.urls))
    ]

You can then link to the password reset form by reversing `"passreset:reset-password"`:

.. code::

   <a href="{% url "passreset:reset-password" %}">Forgot password?</a>

The app takes care of the rest, with the help of django's built-in password
reset workflow. Note that `passreset.urls` an object, not a module. Using
`include('passreset.urls')` will raise an ImportError.

To quickly add password reset functionality to your existing admin, just include
`passreset.admin_urls`:

.. code:: python

    from django.conf.urls.defaults import url, include
    import passreset
    
    urlpatterns = [
      url(r'^admin/passreset/', include(passreset.admin_urls),
      url(r'^admin/', include(admin.site.urls)),
    )

As an added convenience, the passreset app automatically overrides the default
admin site's login template to add a "forgot password?" link.


Namespacing
-----------

If you need multiple password-reset workflows for one site, you must use the
`passreset.urls_ns()` function. Note that you should not use the `namespace`
keyword argument to include:

.. code:: python

    import passreset
    urpatterns = [
        url(r'^profile/reset-password', include(passreset.urls_ns(
            'user-passreset', login_url='/profile/login'))),
        url(r'^staff/reset-password', include(passreset.urls_ns(
            'staff-passreset', login_url='/staff/loging'))),
    ]

If login_url is not supplied, settings.LOGIN_URL is used. You can also pass a 
``template_path`` argument to specify a base path for templates used in the app
instance.

You can then reverse any of the passreset urls using the new namespace:

.. code::
  
  <a href="{% url "staff-passreset:reset-password" %}">Forgot password?</a>


Templates
---------

The default templates form passreset all extend `"passreset/base.html"`, You can
create an override for this template in your project (eg,
`my_project/templates/passreset/base.html`), and have it extend your site's base
template. The templates all use a block called `passreset_content`. So, all you
need to do is include that block inside your site's main content block:

.. code::

   {% extends "mysite/base.html" %}
   {% block content %}
     {% block passreset_content %}
     {% endblock %}
   {% endblock %}

The `urls_ns` function also accepts a `tpl_path` parameter, which allows you to
override any of the templates used by passreset. The path is a template
directory that may contain any of the following: 

* reset_password.html
* done.html
* confirm.html
* complete.html
* email.html
* subject.ttx


Admin
-----

The `passreset.admin_urls` urlconf is basically a convenience shortcut for
`passreset.urls_ns('admin-passreset', login_url='admin:login')`. As stated
above, passreset overrides the default admin login template with a "Forgot
password?" link, which basically looks like this:

.. code:: html

   <a href="{% url admin-passreset:reset-password }">Forgot password?</a>

You can use the admin passreset urls together with another passreset instance
without using namespacing:

.. code:: python

    urlpatterns += patterns('',
      url(r'^admin/passreset/', include(passreset.admin_urls)),
      url(r'^admin/', include(admin.site.urls)),
      url(r'^profile/passreset', include('passreset.urls')),
    )
