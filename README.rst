Django Super Favicon
====================

.. image:: https://api.travis-ci.org/ZuluPro/django-super-favicon.svg
        :target: https://travis-ci.org/ZuluPro/django-super-favicon

.. image:: https://coveralls.io/repos/ZuluPro/django-super-favicon/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/ZuluPro/django-super-favicon?branch=master

Django Super Favicon is a project that aiming to replace external solutions
like `realfavicongenerator.net`_: Create favicon for all kind of client
platform.

Super Favicon does:

- Creates icons in various size
- Uploads them in static file storage (or other)
- Creates HTML headers tags for use them

Why
===

It could sound useless, but hold a website identity in browsers' favorites or
iOS/Android/Windows home screen is a pretty good thing.

I often see that Django dev used to create a view for serve favicon.ico, I
think this is summum of bad pratices: File must be served by a dedicated
server. I designed this project to use Django Storage API and make generated
files deployment agnostic.

There are other Django projects in the same topic:

- `django-favicon`_ : A view for serve favicon (Ouch)
- `django-favicon-plus`_ : Make the same than mine, but through models and ImageField

That's why *super* ...

Install & usage
===============

::

  pip install django-super-favicon

Add the following things in your ``settings.py``: ::

  INSTALLED_APPS = (
      ...
      'favicon',
      ...
  )

Upload them to your storage (by default your filesystem): ::

  ./manage.py generate_favicon your_icon.png

And put this in your templates: ::

  {% load favicon %}
  ...
  <head>
  ...
  {% get_favicons %}
  </head>

It will produce something like: ::

  <link rel="apple-touch-icon-precomposed" href="/static/favicon-152.png">

  <meta name="msapplication-TileColor" content="#FFFFFF">
  <meta name="msapplication-TileImage" content="/static/favicon-144.png">

  <meta name="application-name" content="Name">
  <meta name="msapplication-tooltip" content="Tooltip">
  <meta name="msapplication-config" content="/static/ieconfig.xml">

  <link rel="icon" href="/static/favicon-32.png" sizes="32x32">
  <link rel="icon" href="/static/favicon-57.png" sizes="57x57">
  <link rel="icon" href="/static/favicon-76.png" sizes="76x76">
  <link rel="icon" href="/static/favicon-96.png" sizes="96x96">
  <link rel="icon" href="/static/favicon-120.png" sizes="120x120">
  <link rel="icon" href="/static/favicon-128.png" sizes="128x128">
  <link rel="icon" href="/static/favicon-144.png" sizes="144x144">
  <link rel="icon" href="/static/favicon-152.png" sizes="152x152">
  <link rel="icon" href="/static/favicon-180.png" sizes="180x180">
  <link rel="icon" href="/static/favicon-195.png" sizes="195x195">
  <link rel="icon" href="/static/favicon-228.png" sizes="228x228">
  <link rel="icon" href="/static/smalltile.png" sizes="128x128">
  <link rel="icon" href="/static/mediumtile.png" sizes="270x270">
  <link rel="icon" href="/static/widetile.png" sizes="558x270">
  <link rel="icon" href="/static/largetile.png" sizes="558x558">
  <link rel="shortcut icon" sizes="196x196" href="/static/favicon-196.png">

Settings
========

Super Favicon can be configured with the followings constants in
``settings.py``:

**FAVICON_STORAGE**: Storage class used for store favicons,
default: ``settings.STATICFILES_STORAGE``

**FAVICON_STORAGE_OPTIONS**: Options used for instanciate the custom storage.
default: ``{}``


Management Commands
===================

generate_favicon
----------------

Create favicons in different formats.

    generate_favicon <source_file>

delete_favicon
--------------

Delete previously created favicon

    delete_favicon

Contributing
============

All contribution are very welcomed, propositions, problems, bugs and
enhancement are tracked with `GitHub issues`_ system and patch are submitted
via `pull requests`_.

We use `Travis`_ coupled with `Coveralls`_ as continious integration tools.

.. _`realfavicongenerator.net`: https://realfavicongenerator.net/  
.. _`django-favicon`: https://pypi.python.org/pypi/django-favicon
.. _`django-favicon-plus`: https://github.com/arteria/django-favicon-plus
.. _`Read The Docs`: http://django-super-favicon.readthedocs.org/
.. _`GitHub issues`: https://github.com/ZuluPro/django-super-favicon/issues
.. _`pull requests`: https://github.com/ZuluPro/django-super-favicon/pulls
.. _Travis: https://travis-ci.org/ZuluPro/django-super-favicon
.. _Coveralls: https://coveralls.io/github/ZuluPro/django-super-favicon
