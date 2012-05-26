from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url('^receive$', views.receive, name='receipts.receive'),
)

