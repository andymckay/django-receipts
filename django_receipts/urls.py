from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url('^receive$', views.receive, name='receipts.receive'),
)

