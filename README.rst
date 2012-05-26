Django Receipts
--------------------------------

Parsing of web app receipts in Django. A simple library to parse web
application receipts in Django. It follows the same syntax as the verification
service at thee Mozilla Marketplace.

This is optional, you can just verify your receipt with the Marketplace.
However there are a couple of reasons you might want to do this:

- analytics, tracking usage of your app as it checks receipts

- tracking usage of receipt by IP address to prevent sharing of receipts

- blocking of receipts that you know are fradulent.

This app provides a django model that shows the receipts that been processed,
allowing you to block the receipts there.

Installation
============

Install from pypi::

        pip install django-receipts

Usage
=====

Add `django_receipts` to your `INSTALLED_APPS`::

        INSTALLED_APPS = (...
                'django_receipts',
        )

Run syncdb to install the table::

        python manage.py syncdb

Add in django-receipts into your urls, for example::

       urlpatterns = patterns('',
                ...
                url(r'^receipts/', include('django_receipts.urls')),
       )

You will then be able to do a POST to::

       curl -X POST http://localhost:1234/receiive --data "bogus.receipt"

This will return::

       {"status": "error"}

Since it cannot parse this receipt.

Configuration
=============

* `RECEIPT_CHECK_INTERVAL` (optional): time between receipts from the client to
  actually send receipts to the server. Effectively a cache of the check
  against the server. Default: 60 minutes.
