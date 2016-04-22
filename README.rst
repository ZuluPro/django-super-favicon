Django Super Favicon
====================

.. image:: https://api.travis-ci.org/ZuluPro/django-super-favicon.svg
        :target: https://travis-ci.org/ZuluPro/django-super-favicon

.. image:: https://readthedocs.org/projects/ZuluPro/badge/?version=latest
        :target: https://readthedocs.org/projects/ZuluPro/?badge=latest
        :alt: Documentation Status

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
