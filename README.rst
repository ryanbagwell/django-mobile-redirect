======================
django-mobile-redirect
======================

.. image:: https://circleci.com/gh/ryanbagwell/django-mobile-redirect/tree/master.svg?style=svg&circle-token=e1a063c0881f0c592377120677a8ad969c3a2932
    :target: https://circleci.com/gh/ryanbagwell/django-mobile-redirect/tree/master

Django middleware to redirect mobile devices to the given url.

Installation and Configuration
==============================

Install with pip::

    pip install ...

Add the following to Django settings::

    MIDDLEWARE_CLASSES = [
      'mobile_redirect.middleware.MobileRedirectMiddleware',
    ]

    'MOBILE_REDIRECT_URL' = 'https://github.com/ryanbagwell/django-mobile-redirect'

Requests with user agent strings matching mobile and tablet devices will be
redirected to the specified url

Mobile and tablet devices are defined according to the data at browscap.org_.

.. _browscap.org: http://browscap.org/
